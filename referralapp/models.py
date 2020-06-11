from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoslug import AutoSlugField
from datetime import timedelta
from django.utils import timezone


class Job(models.Model):
	JOB_CATEGORIES = [
		(1,'IT & Software Development'),
		(2,'Products & Services'),
		(3,'Marketing Strategy & Research'),
		(4,'Writing & Transcription'),
		(5,'Business & Customer Service'),
		(6,'Agents & Referral Services'),
		(7,'Data Entry'),
		(8,'Other')
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	job_title = models.CharField(max_length=60,blank=True)
	slug = AutoSlugField(populate_from='job_title',null=True)
	lower_limit = models.PositiveIntegerField(default=0,null=True)
	upper_limit = models.PositiveIntegerField(default=0,null=True)
	job_requirements = models.TextField(blank=True)
	job_category = models.PositiveIntegerField(default=0,choices=JOB_CATEGORIES,null=True)
	job_link = models.CharField(max_length=50,blank=True)
	creation_date = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return self.job_title
	


	class Meta:
		verbose_name_plural = "Jobs"


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
	phonenumber = models.CharField(verbose_name="phone_number", max_length=12,null=True)
	bio = models.TextField(blank=True)


	def __str__(self):
		return self.user.username


class MerchantPromote(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	business_product = models.ImageField(upload_to='images/',null=True)
	business_name = models.CharField(max_length=60,blank=True)
	business_description = models.TextField(blank=True)
	business_charge = models.PositiveIntegerField(default=0,null=True)
	business_link = models.CharField(max_length=100,blank=True)
	profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
	expiry_date = models.DateTimeField(default=timezone.now()+timedelta(days=30))

	def __str__(self):
		return self.business_name

	class Meta:
		verbose_name_plural = "Advertised Merchants"

class FreelanceSkills(models.Model):
	FREELANCE_SKILLS_CHOICES = [
		(1,'Design & Creatives'),
		(2,'Marketing'),
		(3,'Websties & IT'),
		(4,'Accounting'),
		(5,'Legal'),
		(6,'Business Consulting'),
		(7,'Tutoring & Courses'),
		(8,'Trading & Analysis'),
		(9,'Event & Decorations'),
		(10,'Personal Training'),
		(11,'Writing & Transcription'),
		(12,'Photography'),
		(13,'Data Entry Expert')

	]
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	freelance_skill = models.PositiveIntegerField(default=0,choices=FREELANCE_SKILLS_CHOICES,null=True)
	freelance_description = models.TextField(blank=True)
	freelance_charge = models.PositiveIntegerField(default=0,null=True)
	freelance_link = models.CharField(max_length=100,blank=True)
	expiry_date = models.DateTimeField(default=timezone.now()+timedelta(days=30))
	

	def __str__(self):
		return self.user.username 
	
	class Meta:
		verbose_name_plural = "Advertised Skills"




	
class JobPayment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	job_post_paid = models.BooleanField(null=True,default=False)

	def __str__(self):
		return self.user.username
	
	class Meta:
		verbose_name_plural = 'Job Payments'


class BusinessPromotePayment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	business_post_paid = models.BooleanField(null=True,default=False)


	def __str__(self):
		return self.user.username
	
	class Meta:
		verbose_name_plural = 'Business Promote Payments'



class SkillPromotePayment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	skill_post_paid = models.BooleanField(null=True,default=False)

	def __str__(self):
		return self.user.username
	
	class Meta:
		verbose_name_plural = 'Skill Promote Payments'





class Quote(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	CURRENCY_CHOICES = [
		('KES','KES'),
		('USD','USD')
	]
	quote = models.TextField(blank=True)
	currency = models.CharField(max_length=4,choices=CURRENCY_CHOICES,null=True)
	quote_amount = models.PositiveIntegerField(default=0,null=True)
	job = models.ForeignKey(Job,on_delete=models.CASCADE,null=True)
	profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)


	def __str__(self):
		return self.user.username
	
	
	class Meta:
		verbose_name_plural = "Job Quotes"




class Token(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	bid_token = models.PositiveIntegerField(default=0,null=True)

	def __str__(self):
		return self.user.username

	

	class Meta:
		verbose_name_plural = "Eclid tokens"





class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RavePayment(BaseModel):

	amount = models.TextField()
	phone_number = models.TextField()

	def __str__(self):
		return self.phone_number


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
    amount = models.PositiveIntegerField(default=0,null=True)
    phone_number = models.CharField(max_length=12,null=True)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.phone_number

