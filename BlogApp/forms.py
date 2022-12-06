from django import forms
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

#model-based-form for comments
from django import forms
from BlogApp.models import Comment
class CommentForm(forms.ModelForm):
  class Meta:
         model=Comment
         fields=('name','email','body')

class blogLoginForm(forms.Form):
    username=forms.CharField();
    password=forms.CharField(widget=forms.PasswordInput)

class SignupForm(forms.Form):
    name=forms.CharField(label='Enter your name :')
    password=forms.CharField(widget=forms.PasswordInput)
    repassword=forms.CharField(label='Reenter Password',widget=forms.PasswordInput)
    email=forms.EmailField()
    def clean(self):
        total_cleaned_data=super().clean()
        pwd=total_cleaned_data['password']
        rpwd=total_cleaned_data['repassword']
        if pwd!=rpwd:
            raise forms.ValidationError('Both Passwords must be same...!!!')