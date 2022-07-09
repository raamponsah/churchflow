import datetime
from time import sleep

from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.auth_funcs import generate_confirmation_token, decode_token
from accounts.decorators import allowed_roles
from accounts.email import send_mail, generate_confirmation_link_mail
from accounts.forms import RegisterUserForm, UserAccountForm
from django.contrib.auth import login, authenticate, logout

from django.contrib.sites.shortcuts import get_current_site

from accounts.models import ActivateUser, User, UserAccount


def register_user(request):
    register_form = RegisterUserForm()
    context = {'form': register_form}
    if request.method == 'POST':
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            token = generate_confirmation_token(user)
            link = f"{get_current_site(request)}/accounts/confirm-email/{token}"
            generate_confirmation_link_mail(user.email, user.username, link)
            messages.success(request, f'A confirmation email was sent!')

            return redirect('login')
        else:
            context['form'] = register_form
    return render(request, 'accounts/signup.html', context)


def login_user(request):
    page_title = 'Login/Register'
    context = {'page_title': page_title}
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        # this would have to become a custom user (e.g. user)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Ahoy! {user.username}')
            return redirect('dashboard-view')
        else:
            context['login_error'] = 'Email or password is incorrect.'
            return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('register_user')


def sent_confirm_view(request, email):
    context = {'message': f'A confirmation email link has been sent to your email'}
    return render(request, 'accounts/sent_confirmation_link.html', context)


def confirm_email_view(request, token):
    # decode token
    text = decode_token(token)
    url_user_email = text.split('/')[0]
    token_expiry = text.split('/')[1]
    activate_user = ActivateUser.objects.filter(token=token).get()
    if activate_user is not None:
        # ata '2022-04-29 16:45:35.242299
        if datetime.datetime.now() < datetime.datetime.strptime(token_expiry, '%Y-%m-%d %H:%M:%S.%f'):
            if activate_user.user.email == url_user_email:
                user = User.objects.filter(email=url_user_email).get()
                user.is_active = True
                activate_user.is_activated = True
                activate_user.save()
                user.save()
                messages.success(request, f"Email was confirmed successfully")
                print("user activated!")

                return redirect('login')
    return None


def user_account(request):
    user = User.objects.get(id=request.user.id)
    user_account_data = UserAccount.objects.filter(user=user).get()
    user_account_form = UserAccountForm(instance=user_account_data)
    if request.method == 'POST':
        user_account_form = UserAccountForm(request.POST or None, request.FILES, instance=user_account_data)
        if user_account_form.is_valid():
            user_account_form.save()
            messages.success(request,f"Account Updated Successfully")
            return redirect('user_account')
    context = {'form': user_account_form}
    return render(request, 'accounts/user-account.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(user.email, user.username, 'Password Reset', email)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})