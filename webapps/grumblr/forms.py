from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from grumblr.models import *

class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=42,required=True,widget=forms.TextInput(attrs={'class': 'form-control','autofocus':True,'placeholder':'Username'}))
    firstname = forms.CharField(max_length=42,required=True,widget=forms.TextInput(attrs={'class': 'form-control name-1','placeholder':'First Name'}))
    lastname = forms.CharField(max_length=42,required=True,widget=forms.TextInput(attrs={'class': 'form-control name-2','placeholder':'Last Name'}))
    password1=forms.CharField(max_length=42,
                              label='Password',
                              widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    password2 = forms.CharField(max_length=42,
                                label='Confirm Password',
                                required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password confirm'}))
    email=forms.EmailField(max_length=100,
                           label='Email',
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'}))
    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password1=cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username



class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=('user','follower')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'profile-image', 'placeholder': 'FILE'}),
            'introduction': widgets.Textarea(attrs={'class': 'form-control', 'rows': "8",
                                       'placeholder': "420 characters or less introduction."}),
            'age':widgets.NumberInput(attrs={'class': 'form-control','placeholder':'Age'}),
            'telephone':widgets.TextInput(attrs={'class': 'form-control','placeholder':'Telephone like (000)000-0000'}),
            'zipcode':widgets.NumberInput(attrs={'class': 'form-control','placeholder':'Zipcode like 00000'}),
        }
        labels = {
            'image': '',
            'introduction': '',
            'age': '',
            'telephone': '',
            'zipcode': '',
        }
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        if not self.is_valid():
            raise forms.ValidationError("The field you changed is not valid.")
        return cleaned_data



class UserForm(forms.Form):
    firstname = forms.CharField(required=False, max_length=42, widget=forms.TextInput(
        attrs={'class': 'form-control name-1', 'placeholder': 'New First Name','blank':'True'}))
    lastname = forms.CharField(required=False, max_length=42, widget=forms.TextInput(
        attrs={'class': 'form-control name-2', 'placeholder': 'New Last Name','blank':'True'}))
    password0 = forms.CharField(required=False, max_length=42,
                                label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': ' Current Password', 'blank': 'True'}))

    password1 = forms.CharField(required=False, max_length=42,
                                label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': ' New Password','blank':'True'}))

    password2 = forms.CharField(required=False, max_length=42,
                                label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'New Password confirm','blank':'True'}))

    def __init__(self,*args,**kwargs):
        self.user=User.objects.get(username=kwargs.pop("username"))
        super(UserForm,self).__init__(*args,**kwargs)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Two passwords entered did not match.")
        if self.cleaned_data.get('password1') != None and self.cleaned_data.get('password1')!="":
            password0 = self.cleaned_data.get('password0')
            if not self.user.check_password(password0):
                raise forms.ValidationError("Old Passwords is wrong.")
        return cleaned_data

    def save(self,commit=True):
        if self.cleaned_data.get('password1')!="" and self.cleaned_data.get('password1')!=None :
            self.user.set_password(self.cleaned_data['password1'])
        if self.cleaned_data.get('firstname')!= "" and self.cleaned_data.get('firstname')!=None :
            self.user.first_name = self.cleaned_data['firstname']
        if self.cleaned_data.get('lastname')!= "" and self.cleaned_data.get('lastname')!=None :
            self.user.last_name = self.cleaned_data['lastname']
        if commit:
            self.user.save()
        return self.user





class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude=('user','timestamp')
        widgets = {
            'content': widgets.Textarea(attrs={'class': 'form-control','id':'post-event13', 'rows': "4",'placeholder': "Post a short (42 characters or less) message."})
        }
        labels = {
            'content': ''
        }

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        if not self.is_valid():
            raise forms.ValidationError("Post is not valid.")
        return cleaned_data

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content=="" :
            raise forms.ValidationError("Post must not be empty.")
        return content

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=('post','timestamp','user')
        widgets = {
            'content': widgets.Textarea(attrs={'class': 'form-control comment','id':'comment-event13', 'rows': "1",'placeholder': "Make comments."})
        }
        labels = {
            'content': ''
        }

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        if not self.is_valid():
            raise forms.ValidationError("Comment is not valid.")
        return cleaned_data

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content=="" :
            raise forms.ValidationError("Comment must not be empty.")
        return content