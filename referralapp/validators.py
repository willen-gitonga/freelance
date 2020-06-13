from django.core.exceptions import ValidationError
from django import forms
def validate_file_size(value):
    filesize= value.size
    
    if filesize > 204800:
        raise forms.ValidationError("The maximum file size that can be uploaded is 1MB")
    else:
        return value
