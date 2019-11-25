from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def login(request):

    if request.user.is_authenticated:
        return redirect('webserver:index')

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('webserver:index')
    
    else:
        form = AuthenticationForm()
    
    context = {
        'form' : form,
    }
    return render(request, 'webserver/form.html', context)