from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField





class Job(models.Model):
	JOB_CATEGORIES = [
		('Products & Services','Products & Services'),
		('IT & Software Development','IT & Software Development'),
		('Marketing Strategy & Research','Marketing Strategy & Research'),
		('Writing & Transcription','Writing & Transcription'),
		('Business & Customer Service','Business & Customer Service'),
		('Agents & Referral Services','Agents & Referral Services'),
		('Other','Other')
	]
	SOCIAL_CATEGORIES = [
		('Digital Media Marketing','I need more traffic to my online business'),
		('E-commerce Specialist Required','I need an E-commerce Specialist')
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	job_title = models.CharField(max_length=60,blank=True)
	slug = AutoSlugField(populate_from='job_title',null=True)
	lower_limit = models.FloatField(null=True,default=0.0)
	upper_limit = models.FloatField(null=True,default=0.0)
	job_completion = models.PositiveIntegerField(default=0,null=True)
	job_requirements = models.TextField(blank=True)
	job_category = models.CharField(max_length=60,choices=JOB_CATEGORIES,blank=True)
	digital_category = models.CharField(max_length=60,choices=SOCIAL_CATEGORIES,blank=True)
	job_link = models.CharField(max_length=100,blank=True)
	creation_date = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return self.job_title
	


	class Meta:
		verbose_name_plural = "Jobs"

class JobPayment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	job_post_paid = models.BooleanField(null=True,default=False)

	def __str__(self):
		return self.user.username
	
	class Meta:
		verbose_name_plural = 'Job Payments'

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
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	bid_token = models.PositiveIntegerField(default=0,null=True)

	def __str__(self):
		return self.user.username

	

	class Meta:
		verbose_name_plural = "Eclid tokens"

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
	phonenumber = models.CharField(verbose_name="phone_number", max_length=12,null=True)
	bio = models.TextField(blank=True)


	def __str__(self):
		return self.user.username



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name