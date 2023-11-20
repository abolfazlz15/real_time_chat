from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

from auths.forms import UserRegisterForm


def register(request): 
    if request.method == 'POST':
        form  = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat:index')
            return redirect('auths:login')
    else:
        form = UserRegisterForm()
    return render(request, 'auths/register.html', {'form': form})