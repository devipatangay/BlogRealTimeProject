from django import forms
class EmailSendForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()
    comments=forms.CharField(required=False,widget=forms.Textarea)

#model-based-form for comments
from django import forms
from BlogApp.models import Comment,Post
class CommentForm(forms.ModelForm):
  class Meta:
         model=Comment
         fields=('name','email','body')


from django.contrib.auth.models import User
class Signupform(forms.ModelForm):
     class meta:
         model=User
         fields = ['first name','last name','password','username','email']

class postform(forms.ModelForm):
     class Meta:
       model = Post
       fields ='__all__'






