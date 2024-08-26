from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.conf import settings

def signup(request):
    form=UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()

        return redirect(settings.LOGIN_URL)

    context = {'form':form}
    return render(request,'registration/signup.html',context)