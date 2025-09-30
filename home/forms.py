from django import forms
from datetime import date

class bookingform(forms.Form):
    pick = forms.CharField(max_length=20)
    drop = forms.CharField(max_length=20)
    seat = forms.IntegerField()
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date','min': date.today().strftime('%Y-%m-%d')}),label="select booking date")
    passanger_name = forms.CharField(max_length=20)
    email_id = forms.CharField(max_length=20)
    phone_no = forms.CharField(max_length=20)


    def clean_booking_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise forms.ValidationError("Past dates are not allowed.")
        return selected_date
