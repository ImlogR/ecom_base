from django.db import models
import uuid

from django.contrib.auth.models import User

class customer(models.Model):
    user= models.OneToOneField(User, related_name='user_name', on_delete=models.CASCADE, null=True, blank=True)
    name= models.CharField(max_length=200, null=True)
    email= models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

class product(models.Model):
    owner= models.ForeignKey(User, related_name='owner_name', on_delete=models.CASCADE, blank=True, null=True)
    name= models.CharField(max_length=200, null=True)
    price= models.DecimalField(max_digits=17, decimal_places=2, null=True)
    digital= models.BooleanField(default=False, null=False, blank=False)
    image= models.ImageField(null=True, blank=True)
    
    #solution fo rendering null/blank image url
    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url= ''
        return url

    def __str__(self):
        return self.name
    
class order(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    customer= models.ForeignKey(customer, related_name='ordering_customer', on_delete=models.CASCADE, blank=True, null=True)
    date_ordered= models.DateTimeField(auto_now_add= True)
    complete= models.BooleanField(default=False, null=True, blank=False)
    transaction_id= models.CharField(max_length=20, null=True, blank=True)

    @property
    def get_cart_total(self):
        orderitems= self.orderid.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems= self.orderid.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping= False
        orderitems= self.orderid.all()
        for i in orderitems:
            if i.product.digital== False:
                shipping= True
        
        return shipping

    def __str__(self):
        return str(self.id)
    
class orderItems(models.Model):
    product= models.ForeignKey(product,related_name='product_name', on_delete=models.CASCADE, blank=True, null=True)
    order= models.ForeignKey(order, related_name='orderid', on_delete= models.CASCADE, blank=True, null=True)
    quantity= models.IntegerField(default=0, null=True, blank=True)
    date_added= models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total= self.product.price * self.quantity
        return total
    
class shippingAddress(models.Model):
    customer= models.ForeignKey(customer,related_name='customer_address', on_delete=models.SET_NULL, blank=True, null=True)
    order= models.ForeignKey(order, related_name='shipping_order',on_delete=models.SET_NULL, blank=True, null=True)
    address= models.CharField(max_length=200, null=True)
    city= models.CharField(max_length=200, null=True)
    state= models.CharField(max_length=200, null=True)
    zipcode= models.CharField(max_length=200, null=True)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

