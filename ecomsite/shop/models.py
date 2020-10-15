from django.db import models
from django.conf import settings

# Create your models here.
class Maincategories(models.Model):
	MainCategory = models.CharField(max_length=200)
	MainCategory_image = models.ImageField(upload_to='category/',default='category/default.jpg')

	def __str__(self):
		return self.MainCategory

class Subcategories(models.Model):
	MainCategory = models.ForeignKey(Maincategories,on_delete=models.CASCADE)
	SubCategory = models.CharField(max_length=200)
	SubCategory_image = models.ImageField(upload_to='subcategory/',default='subcategory/default.jpg')

	def __str__(self):
		return self.SubCategory

class Products(models.Model):
	title = models.CharField(max_length=200)
	SubCategory = models.ForeignKey(Subcategories,on_delete=models.CASCADE,blank=True,null=True)
	image = models.ImageField(upload_to='Products/',default='/Products/default.jpg')
	description = models.TextField()
	price = models.FloatField()
	discount_price = models.FloatField(blank=True,null=True)

	def __str__(self):
		return self.title

class OrderItem(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		blank=True,
		null=True)
	item = models.ForeignKey(Products,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	ordered = models.BooleanField(default=False) 

	def __str__(self):
		return f"{self.quantity} of {self.item.title}"

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_total_discount_item_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_total_discount_item_price()

	def get_final_price(self):
		if self.item.discount_price:
			 return self.get_total_discount_item_price()
		return self.get_total_item_price()


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		blank=True,
		null=True)
	items = models.ManyToManyField(OrderItem)
	start_date = models.DateTimeField(auto_now_add=True)
	ordered_date = models.DateTimeField()
	ordered = models.BooleanField(default=False)
	billing_address = models.ForeignKey('Billing_Address',on_delete=models.SET_NULL,blank=True,
		null=True)

	def __str__(self):
		return self.user.username

	def get_total(self):
		total = 0 
		for order_item in self.items.all():
			total += order_item.get_final_price()
		# if self.coupon:
		# 	total -= self.coupon.amount
		return total

class Billing_Address(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	address = models.CharField(max_length=1000)
	landmark = models.CharField(max_length=300)
	city = models.CharField(max_length=300)
	country = models.CharField(max_length=200)
	zipcode = models.CharField(max_length=200)

	def __str__(self):
		return self.user.username