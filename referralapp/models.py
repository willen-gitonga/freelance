from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField





class Job(models.Model):
	LOWER_LIMIT =[
		(0.5,'0.5$-1.0$'),
		(1,'1.0$-1.5$'),
		(1.5,'1.5$-2.0$'),
		(2,'2.0$-2.5$'),
		(3,'3.0$-3.5$')

	]
	UPPER_LIMIT =[
		(1.0,'0.5$-1.0$'),
		(1.5,'1.0$-1.5$'),
		(2.0,'1.5$-2.0$'),
		(2.5,'2.0$-2.5$'),
		(3.5,'3.0$-3.5$')

	]

	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	job_title = models.CharField(max_length=250,blank=True)
	slug = AutoSlugField(populate_from='job_title',null=True)
	lower_limit = models.FloatField(choices=LOWER_LIMIT,default=0.0)
	upper_limit = models.FloatField(choices=UPPER_LIMIT,default=0.0)
	job_completion = models.PositiveIntegerField(default=0,null=True)
	job_requirements = models.TextField(blank=True)
	creation_date = models.DateTimeField(auto_now_add=True,null=True)
	def __str__(self):
		return self.job_title
	


	class Meta:
		verbose_name_plural = "Jobs"



class Quote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	CURRENCY_CHOICES = [
		('KES','KES'),
		('USD','USD')
	]
	quote = models.TextField(blank=True)
	currency = models.CharField(max_length=4,choices=CURRENCY_CHOICES,null=True)
	quote_amount = models.DecimalField(max_digits=15, decimal_places=1, default=0.0)
	job = models.ForeignKey(Job,on_delete=models.CASCADE,null=True)

	
	
	class Meta:
		verbose_name_plural = "Job Quotes"




class Token(models.Model):
	TOKEN_PRICES =[
		(3,'3 credits - KES 300'),
		(5,'5 credits - KES 500'),
		(7,'7 credits - KES 700')
	]
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	token_price = models.IntegerField(choices=TOKEN_PRICES,default=0)
	bid_token = models.PositiveIntegerField(default=0,null=True)


	def __str__(self):
		return self.user.username

	

	class Meta:
		verbose_name_plural = "Eclid tokens"


class ConfirmPayment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	payment_number = models.CharField(max_length=10,null=True)
	mpesa_code = models.CharField(max_length=12,null=True)


	def __str__(self):
		return self.payment_number
	
	class Meta:
		verbose_name_plural = "Payment Confirmed"

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
	date_joined = models.DateTimeField(auto_now_add=True,null=True)
	first_name = models.CharField(max_length=15,blank=True)
	last_name = models.CharField(max_length=15,blank=True)
	bio = models.TextField(blank=True)

	

	def __str__(self):
		return self.user.username

