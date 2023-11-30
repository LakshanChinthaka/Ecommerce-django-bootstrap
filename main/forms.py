from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
# from .models import ProductReview,UserAddressBook
from django.contrib.auth.forms import AuthenticationForm
from .models import UserAddressBook

# #create form text feilds 
# class SignupForm(UserCreationForm):
    
    
# 	class Meta:
# 		model=User
# 		fields=('first_name','last_name','email','username','password1','password2')
class SignupForm(UserCreationForm):
    mobile1 = forms.CharField(max_length=50, required=False, label='Mobile Number 1')
    mobile2 = forms.CharField(max_length=50, required=False, label='Mobile Number 2')
    address = forms.CharField(widget=forms.Textarea, required=False, label='Address')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'mobile1', 'mobile2', 'address']
  
# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('address','mobile','mobile2','status')
  
# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=User
		fields=('first_name','last_name','email','username')
  
# from django import forms
# from django.contrib.auth.forms import UserCreationForm


# class CustomUserCreationForm(UserCreationForm):
#     mobile1 = forms.CharField(max_length=50, required=False)
#     mobile2 = forms.CharField(max_length=50, required=False)
#     address = forms.CharField(widget=forms.Textarea, required=False)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'mobile1', 'mobile2', 'address']



