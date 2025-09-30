from django import forms
from .models import sign

class SignForm(forms.Form):
    name = forms.CharField(max_length=20)
    phone_no = forms.IntegerField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']
        if sign.objects.filter(phone_no=phone_no).exists():
            raise forms.ValidationError("Phone number already registered.")
        return phone_no

    def clean_email(self):
        email = self.cleaned_data['email']
        if sign.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

class loginform(forms.Form):
    name = forms.CharField()
    phone_no = forms.IntegerField()
    password = forms.CharField()


