from django.contrib.auth.forms import UserCreationForm
from accounts.models import Shopper 
from django import forms 


class SignUpForm (UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    
    class Meta:
        model = Shopper
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = ''
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].help_text = ''
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].help_text = ''
        

"""
    email = forms.EmailField(label='', widget= forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    
    class Meta:
        model = Shopper
        fields= ('username','email','password')
   def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''   
"""        
 