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

		self.fields['password2'].widget.attrs = {
			'placeholder': 'Password Confirmation',
		}
		self.fields['password2'].label = ''


		

	

	class Meta:
		model = User
		fields = ('username','email','password1','password2','date_joined')
	



class TokenForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(TokenForm, self).__init__(*args, **kwargs)
		self.fields['token_price'].label = 'Select the number of E-tokens to purchase'


	class Meta:
		model = Token
		fields = ('token_price',)



	

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





class ProfileEditForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(ProfileEditForm, self).__init__(*args, **kwargs)
		self.fields['bio'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Write your bio highlighting how fast you can complete a task and the quality of your work.',
		}
		self.fields['bio'].label = ''

			
		self.fields['bio'].required = True

		self.fields['last_name'].widget.attrs = {
			'placeholder':'Last Name'
		}

		self.fields['last_name'].label = ''
		self.fields['last_name'].required = True

		self.fields['first_name'].widget.attrs = {
			'style':'margin-top:20px',
			'placeholder':'First Name'
		}

		self.fields['first_name'].label = ''
		self.fields['first_name'].required = True



		


	class Meta:
		model = Profile
		fields = ('first_name','last_name','bio')




class ProfileCreationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):

		super(ProfileCreationForm, self).__init__(*args, **kwargs)
		self.fields['bio'].widget.attrs = {
			'style':'height:240px;',
			'placeholder': 'Write your bio highlighting how fast you can complete a task and the quality of your work.',
		}
		self.fields['bio'].label = ''

			
		self.fields['bio'].required = True

		self.fields['last_name'].widget.attrs = {
			'placeholder':'Last Name'
		}

		self.fields['last_name'].label = ''
		self.fields['last_name'].required = True

		self.fields['first_name'].widget.attrs = {
			'style':'margin-top:20px',
			'placeholder':'First Name'
		}

		self.fields['first_name'].label = ''
		self.fields['first_name'].required = True



		


	class Meta:
		model = Profile
		fields = ('first_name','last_name','bio')
		
		






    