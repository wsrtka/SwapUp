from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .decorators import unauthenticated_user
from exchange.models import Student

@unauthenticated_user
def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            user = form.save()
            user.save()
            
            student, created = Student.objects.get_or_create(index_number = form.cleaned_data.get('index'))

            if created:
                student.index_number = form.cleaned_data.get('index')
                
            student.semester = form.cleaned_data.get('semester')  
            student.user = user
            student.save()

            username = form.cleaned_data.get('username')

            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')