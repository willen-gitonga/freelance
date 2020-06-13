from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Token,Profile,Job,Quote,FreelanceSkills,MerchantPromote
from .validators import validate_file_size


	
class SignupForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs = {
			'placeholder': 'First Name',
		}
		self.fields['first_name'].label = ''
		self.fields['first_name'].required = True 

		self.fields['last_name'].widget.attrs = {
			'placeholder': 'Last Name',
		}
		self.fields['last_name'].label = ''
		self.fields['last_name'].required = True 

		self.fields['username'].widget.attrs = {
			'placeholder': 'Username',
		}
		self.fields['username'].label = ''

		self.fields['email'].widget.attrs = {
			'placeholder': 'Email address',
		}
		self.fields['email'].label = ''
		self.fields['email'].required = True 

		self.fields['password1'].widget.attrs = {
			'placeholder': 'Password',
		}
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = None

		self.fields['password2'].widget.attrs = {
			'placeholder': 'Password Confirmation',
		}
		self.fields['password2'].label = ''


	def clean_email(self):
		email_address = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email_address)
		if qs.exists():
			raise forms.ValidationError("The email you've chosen is already registered.")
		return email_address
		
	email = forms.EmailField()
	
	class Meta:
		model = User
		fields = ('first_name','last_name','username','email','password1','password2')
	




class JobQuoteForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):

		super(JobQuoteForm, self).__init__(*args, **kwargs)
		self.fields['quote'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Let the employer know you are the best person for the job.Show that you can complete the task in adequate time.Also include your job rate amount.',

		}
		self.fields['quote'].label = 'My Offer:'

			
		self.fields['quote'].required = True
		self.fields['quote_amount'].label = 'Job Rate'
			
	class Meta:
		model = Quote
		fields = ('quote','currency','quote_amount') 



class PostJobForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):

		super(PostJobForm, self).__init__(*args, **kwargs)
		self.fields['job_requirements'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Give a brief description of what your project entails.',
		}
		self.fields['job_requirements'].label = ''
		self.fields['job_requirements'].required = True

		self.fields['job_title'].widget.attrs = {
			'placeholder': 'What is the title of your project?',
		}
		self.fields['job_title'].label = ''
		self.fields['job_title'].required = True
		self.fields['job_title'].help_text = 'The title can be something like: I need a software designed'


		self.fields['lower_limit'].label = 'Least amount you will be paying top candidates? - KES'
		self.fields['lower_limit'].required = True

		
		self.fields['upper_limit'].label = 'Highest amount you will be paying top candidates? - KES'
		self.fields['upper_limit'].required = True
		
		self.fields['job_category'].label = 'Choose a category for your project from the list'
		self.fields['job_category'].required = True

		self.fields['job_link'].widget.attrs = {
			'placeholder': 'Link to similar project',
			'input_type':'url',
		}
		self.fields['job_link'].label = ''
		self.fields['job_link'].required = False
		self.fields['job_link'].help_text = 'This can be a link to any sample project.You can only paste one link.'


	class Meta:
		model = Job
		fields = ('job_title','job_category','job_requirements','job_link','lower_limit','upper_limit')


class DigitalMediaForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):

		super(DigitalMediaForm, self).__init__(*args, **kwargs)

		self.fields['business_description'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Description of what products you sell.Show that the quality of your products is superb and the prices are pocket friendly to customers.You can also include where you are based.',
		}
		self.fields['business_description'].label = ''
		self.fields['business_description'].required = True

		self.fields['business_name'].widget.attrs = {
			'placeholder': 'Name of your business?',
		}
		self.fields['business_name'].label = ''
		self.fields['business_name'].required = True

		self.fields['business_charge'].label = 'How much do you sell your products at? - KES'
		self.fields['business_charge'].required = True
		self.fields['business_charge'].help = 'All currencies should be in kenyan shillings.'

		self.fields['business_link'].widget.attrs = {
			'placeholder': 'Link to more products my business sells',
			'input_type':'url',
		}
		self.fields['business_link'].label = ''
		self.fields['business_link'].required = True
		self.fields['business_link'].help_text = 'This is a link to your online store,site or social media page.You can only paste one link.Product does not only apply to tangible goods.'

		self.fields['business_product'].label = 'Image of product your business sells'
		self.fields['business_product'].required = True
		self.fields['business_product'].help_text = 'Maximum image size 200KB.jpg,jpeg,png only'

	business_product = forms.ImageField(validators=[validate_file_size])

	class Meta:
		model = MerchantPromote
		fields = ('business_name','business_description','business_product','business_charge','business_link')


class FreelanceSkillAdvertiseForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(FreelanceSkillAdvertiseForm, self).__init__(*args, **kwargs)

		self.fields['freelance_description'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Description of what you do.Show your level experience,the good quality of your work and technologies you are proficient in if any.This will attract more clients who view your promoted skill.',
		}
		self.fields['freelance_description'].label = ''
		self.fields['freelance_description'].required = True

		
		self.fields['freelance_skill'].label = 'Choose the type of skill you want to promote from the list below.'
		self.fields['freelance_skill'].required = True

		self.fields['freelance_charge'].label = 'How much do you normally charge? - KES'
		self.fields['freelance_charge'].required = True
		self.fields['freelance_charge'].help = 'All currencies should be in kenyan shillings.'

		self.fields['freelance_link'].widget.attrs = {
			'placeholder': 'Link to my best work',
			'input_type':'url',
		}
		self.fields['freelance_link'].label = ''
		self.fields['freelance_link'].required = True
		self.fields['freelance_link'].help_text = 'This can be a link to your social media showing your previous work,a link to your portfolio showing your previous work or google drive link.You can paste one link only.Maximum 100 characters.If the link is too long use a url shortener and then add it.'


	class Meta:
		model = FreelanceSkills
		fields = ('freelance_skill','freelance_description','freelance_charge','freelance_link')



class RegisterProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(RegisterProfileForm, self).__init__(*args, **kwargs)
		self.fields['phonenumber'].widget.attrs = {
			'placeholder': '2547xxxxxxxx',
		}
		self.fields['phonenumber'].required = True
		self.fields['phonenumber'].label = 'Enter phone number'
		self.fields['phonenumber'].help_text = 'Enter your phone number starting with country code 254 without the plus sign(+).'


	def clean_phonenumber(self):
		phone_number = self.cleaned_data.get('phonenumber')
		qs = Profile.objects.filter(phonenumber=phone_number)
		if qs.exists():
			raise forms.ValidationError("The phone number is already registered.")
		return phone_number
	phonenumber = forms.CharField(
		max_length=12,
	
	)

	class Meta:
		model = Profile
		fields = ('phonenumber',)




class ProfileCreationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(ProfileCreationForm, self).__init__(*args, **kwargs)
		self.fields['bio'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Write your bio highlighting how fast you can complete a task and the quality of your work.',
		}
		self.fields['bio'].label = ''
		self.fields['bio'].required = True


	class Meta:
		model = Profile
		fields = ('bio',)


		
		






    