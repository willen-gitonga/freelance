from django.test import TestCase

# Create your tests here.


 class Meta:
	    model = User
        fields = ('username','first_name','last_name','Phone_Number','Email','password1','password2')

	def clean_password(self):
		cleaned_data = self.cleaned_data
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 != password2:
			raise forms.ValidationError("Passwords don't match.")
		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("The username you have chosen is unavailable.")
		return username

	def clean_email(self):
		email_address = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email_address)
		if qs.exists():
			raise forms.ValidationError("The email you've chosen is already registered.")
		return email_address

    def clean_phoneNumber(self):
        phone_number = self.cleaned_data.get('Phone_Number')
        qs = User.objects.filter(Phone_Number=phone_number)
        if qs.exists():
            raise forms.ValidationError("The phone number you've entered is already registred.")
        return phone_number
