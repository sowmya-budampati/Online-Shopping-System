from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    CITY_CHOICES = [
        ('London','London'),
        ('Windsor','Windsor'),
        ('Bramton','Bramton'),
        ('Waterloo','Waterloo')
    ]
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=10, choices=CITY_CHOICES, default='Windsor')

    def __str__(self):
       #return 'Warehouse is {}.'.format(self.warehouse)
        return 'Category name is {0} , warehouse at {1}.'.format(self.name,self.warehouse)


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'The price of {0} is {1}.'.format(self.name,self.price)

    def refill(self):
        st = self.stock + 100
        t = Product.objects.get(name=self.name)
        t.stock = st
        t.save()


class Client(User):
     PROVINCE_CHOICES = [
         ('AB', 'Alberta'),
         ('MB', 'Manitoba'),
         ('ON', 'Ontario'),
         ('QC', 'Quebec'),
     ]
     company = models.CharField(max_length=50, null=True, blank=True)
     shipping_address = models.CharField(max_length=300, null=True, blank=True)
     city = models.CharField(max_length=20, default='Windsor')
     province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
     interested_in = models.ManyToManyField(Category)

     def __str__(self):
         # return 'Warehouse is {}.'.format(self.warehouse)
         return 'Company name is {0} , located at {1}.'.format(self.company, self.city)


class Order(models.Model):
        VALID_CHOICES = [
            (0, 'Order Cancelled'),
            (1, 'Order Placed'),
            (2, 'Order Shipped'),
            (3, 'Order Delivered')
        ]
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        client = models.ForeignKey(Client, on_delete=models.CASCADE)
        num_unit = models.PositiveIntegerField(default=1)
        order_status = models.IntegerField(choices=VALID_CHOICES, default=1)
        status_date = models.DateField(default=timezone.now)

        def __str__(self):
            cost = self.product.price * self.num_unit
            return 'Order# ' + str(self.id) + ': For ' + ' ' + self.product.name + " (#) by " + str(
                self.client) + ' and total amount is ' + str(cost)
