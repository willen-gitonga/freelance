from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Token,Profile,Job,Quote



class SigninForm(forms.Form):
    username = forms.CharField(
		label='',
		widget=forms.TextInput(

			attrs={
				"placeholder": "Username",
				
			}
		))
    password = forms.CharField(
		label='',
		widget=forms.PasswordInput(attrs={
				"placeholder": "Password",
				
			}))
	
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
			'placeholder': 'Let the client know you are the best person for the job.Show that you can complete the task in adequate time.Also include your job rate.',

		}
		self.fields['quote'].label = 'My Quote:'

			
		self.fields['quote'].required = True
		self.fields['quote_amount'].label = 'Job Rate/hrs'
			
	class Meta:
		model = Quote
		fields = ('quote','currency','quote_amount') 



class PostJobForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):

		super(PostJobForm, self).__init__(*args, **kwargs)
		self.fields['job_requirements'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Give a brief description of what your job entails.',
		}
		self.fields['job_requirements'].label = ''
		self.fields['job_requirements'].required = True

		self.fields['job_title'].widget.attrs = {
			'placeholder': 'What is the title of your job?',
		}
		self.fields['job_title'].label = ''
		self.fields['job_title'].required = True
		self.fields['job_title'].help_text = 'The title can be something like: I need a software designed'


		self.fields['lower_limit'].label = 'Least amount you will be spending? - KES'
		self.fields['lower_limit'].required = True

		
		self.fields['upper_limit'].label = 'Highest amount you will be spending? - KES'
		self.fields['upper_limit'].required = True
		
		self.fields['job_category'].label = 'Choose a category for your job'
		self.fields['job_category'].required = True

		self.fields['job_link'].widget.attrs = {
			'placeholder': 'Paste Your Link Here',
			'input_type':'url',
		}
		self.fields['job_link'].label = ''
		self.fields['job_link'].required = False
		self.fields['job_link'].help_text = 'This can be a link to any sample project,your online shop,social media page or Agent link.You can only paste one link.'


	class Meta:
		model = Job
		fields = ('job_title','job_category','job_requirements','job_link','lower_limit','upper_limit')


class DigitalMediaForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):

		super(DigitalMediaForm, self).__init__(*args, **kwargs)

		self.fields['job_requirements'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Description of what your business does.Also include contact details that customers can reach you on directly.',
		}
		self.fields['job_requirements'].label = ''
		self.fields['job_requirements'].required = True

		self.fields['job_title'].widget.attrs = {
			'placeholder': 'Name of your business?',
		}
		self.fields['job_title'].label = ''
		self.fields['job_title'].required = True

		self.fields['lower_limit'].label = 'Least amount you will be paying to top candidates? - KES'
		self.fields['lower_limit'].required = True
		self.fields['lower_limit'].help = 'All currencies should be in kenyan shillings.'

		
		self.fields['upper_limit'].label = 'Highest amount you will be paying to top candidates? - KES'
		self.fields['upper_limit'].required = True
		self.fields['upper_limit'].help = 'All currencies should be in kenyan shillings.'

		

		self.fields['digital_category'].label = 'What solution are you looking for?'
		self.fields['digital_category'].required = True

		self.fields['job_link'].widget.attrs = {
			'placeholder': 'Link to my online business',
			'input_type':'url',
		}
		self.fields['job_link'].label = ''
		self.fields['job_link'].required = True
		self.fields['job_link'].help_text = 'Link to your online shop,site or social media page.You can only paste one link.'


	class Meta:
		model = Job
		fields = ('job_title','digital_category','job_requirements','lower_limit','upper_limit','job_link')

class RegisterProfileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(RegisterProfileForm, self).__init__(*args, **kwargs)
		self.fields['phonenumber'].widget.attrs = {
			'placeholder': 'Phone Number 2547xxxxxxxx',
		}
		self.fields['phonenumber'].required = True
		self.fields['phonenumber'].label = ''
		self.fields['phonenumber'].help_text = 'Input your phone number starting with 254 without the plus sign(+).'


	def clean_phonenumber(self):
		phone_number = self.cleaned_data.get('phonenumber')
		qs = Profile.objects.filter(phonenumber=phone_number)
		if qs.exists():
			raise forms.ValidationError("The phone number is already registered.")
		return phone_number
	phonenumber = forms.CharField(
		min_length=12,
	
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
		
		






    