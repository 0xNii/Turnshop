from django import forms
from .models import Profile,SignUp
 
class ImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class EmailSignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['email']