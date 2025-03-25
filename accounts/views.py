from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, UsernameOrEmailAuthenticationForm,ForgotPasswordForm,SetNewPasswordForm
# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UsernameOrEmailAuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username_or_email = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                # Try to fetch the user by username or email
                User = get_user_model()  # Use get_user_model to fetch the user model
                try:
                    if '@' in username_or_email:
                        user = User.objects.get(email=username_or_email)
                    else:
                        user = User.objects.get(username=username_or_email)
                except User.DoesNotExist:
                    # Username or email is incorrect
                    if '@' in username_or_email:
                        form.add_error('username', "This email is not registered.")
                    else:
                        form.add_error('username', "This username does not exist.")
                else:
                    # Username or email is correct, now check the password
                    user = authenticate(request, username=user.username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('/')  # Redirect to the home page or dashboard
                    else:
                        # Password is incorrect
                        form.add_error('password', "The password is incorrect.")
        else:
            form = UsernameOrEmailAuthenticationForm()

        context = {'form': form}
        return render(request, 'accounts/login.html', context)
    else:
        return redirect('/')
    

@login_required 
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request,messages.SUCCESS,'your account has been created.')
                return redirect('/')
            else:
                messages.add_message(request,messages.ERROR,'your account didnt create.')
        form = CustomUserCreationForm()
        context = {'form':form}
        return render(request,'accounts/signup.html',context)
    else:
        return redirect('/')
