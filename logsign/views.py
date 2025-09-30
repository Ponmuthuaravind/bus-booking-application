from django.shortcuts import render,redirect
from .models import sign
from .forms import SignForm,loginform


# Create your views here.


def signView(request):
    if request.method == 'POST':
        form = SignForm(request.POST)
        if form.is_valid():
            name =form.cleaned_data['name']
            phone_no = form.cleaned_data['phone_no']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            sign.objects.create(name = name,phone_no = phone_no,email = email,password = password,confirm_password = confirm_password)
        else:
            return render(request,'sign.html',{'form':form})
    form = SignForm()
    return render(request,'sign.html',{'form':form})




from django.shortcuts import render, redirect
from .models import sign
from .forms import loginform

def loginview(request):
    error = ''
    pass_error = ''
    ph_error =''
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_no = form.cleaned_data['phone_no']
            password = form.cleaned_data['password']

            # SAFELY get first matching user
            user = sign.objects.filter(name=name).first()

            if user:
                if user.password == password:
                    if user.phone_no == phone_no:
                        return redirect('home', person=name)
                    else:
                        ph_error = "Incorrect phone number"
                else:
                    pass_error = "Incorrect password."
            else:
                error = "User not found."
    else:
        form = loginform()
        
    return render(request, 'login.html', {'form': form, 'error': error,'pass_error':pass_error,'ph_error':ph_error})
