import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

User = get_user_model()

# Create your models here.
class Categories(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name          = models.CharField(max_length=50, blank=False, null=False)
    description   = models.JSONField(blank=False, null=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Products(models.Model):
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image               = models.FileField(upload_to='product/product_images/', blank=False, null=False, default="None")
    image1              = models.FileField(upload_to='product/product_images/', blank=True, null=True)
    image2              = models.FileField(upload_to='product/product_images/', blank=True, null=True)
    name                = models.CharField(max_length=50, blank=False, null=False)
    description         = models.TextField(blank=False, null=False)
    category            = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price               = models.FloatField(default=0.0, blank=False, null=False)
    merchant_price      = models.IntegerField(default=0.0, blank=False, null=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Products"


class Orders(models.Model):
    ord_id               = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer             = models.ForeignKey(User, on_delete=models.CASCADE)
    product              = models.ForeignKey(Products, on_delete=models.CASCADE)
    ord_quantity         = models.IntegerField(default=0, blank=False, null=False)
    ord_price            = models.FloatField(default=0.0, blank=False, null=False)
    ord_date             = models.DateTimeField(auto_now_add=True)
    ord_status           = models.CharField(max_length=50, blank=False, null=False, default='Pending')
    ord_feedback         = models.TextField(blank=True, null=True)
    ord_image            = models.FileField(upload_to='order/customised_images/', blank=True, null=True)
    cancellation_status  = models.CharField(max_length=50, blank=False, null=False, default='No')
    cancellation_date    = models.DateTimeField(blank=True, null=True)
    cancellation_reason  = models.TextField(blank=True, default="None")
    user_gst_num         = models.CharField(max_length=100, blank=True, default='Not Provided')
    user_refund_cheque   = models.FileField(upload_to='order/OrderRefund/', blank=True)

    def __str__(self):
        return self.customer.email
    
    def save(self, *args, **kwargs):
        gst = (self.product.price*self.ord_quantity) * 0.18
        self.ord_price = (self.product.price*self.ord_quantity) + gst
        super().save()
    
    class Meta:
        verbose_name_plural = "Orders"


class Coupon(models.Model):
    name = models.CharField(verbose_name="Coupon Name", max_length=40, primary_key=True, unique=True)
    discount = models.FloatField(verbose_name="Discount Percent", max_length=40, default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Coupons"


@receiver(post_save, sender=Orders)
def send_an_email(sender, created, **kwargs):
    if created:
        orderID = kwargs['instance']
        msg =f"Your order for {orderID.product.name} has been placed successfully!\nYour Order Details are ~ \nOrder ID is → {orderID.ord_id}\nProduct Name → {orderID.product.name}\nCategory → {orderID.product.category.name}\nOrder Price(including GST) → {orderID.ord_price}\nOrder Date → {orderID.ord_date}\nOrder Status → {orderID.ord_status}"
        send_mail(subject='Order Placed Successfully!', message=msg, from_email='dehimangshu2020@gmail.com', recipient_list=[orderID.customer.email], fail_silently=False)
