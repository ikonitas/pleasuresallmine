from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_after_registration
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from automated_emails.views import send_welcome_email, send_admin_welcome_email
from accounts.models import UserProfile, Address
from accounts.forms import RegistrationForm, LoginForm, UserProfileForm, AddressForm
from accounts.forms import RegistrationFormAdmin
from accounts.utils import generate_username, get_pronounceable_password

@transaction.commit_on_success
def login_register(request, *args):
    next_url = '/'
    message = None
    if request.GET.has_key('next'):
        next_url = request.GET.get('next')
    if request.method == 'POST':
        if "register" in request.POST:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                username = generate_username(
                        registration_form.cleaned_data['first_name'],
                        registration_form.cleaned_data['last_name']
                )
                user = User.objects.create_user(
                        username,
                        registration_form.cleaned_data['email'],
                        registration_form.cleaned_data['password'],
                )
                user.first_name = registration_form.cleaned_data['first_name']
                user.last_name = registration_form.cleaned_data['last_name']
                user.is_active = True
                user.save()

                user_profile = UserProfile()
                user_profile.title = registration_form.cleaned_data['title']
                user_profile.date_of_birth = registration_form.cleaned_data['date_of_birth']
                user_profile.phone = registration_form.cleaned_data['phone']
                user_profile.user = user
                user_profile.terms = registration_form.cleaned_data['terms']

                user_profile.save()
                # Billing address
                address = Address()
                address.line_1 = registration_form.cleaned_data['line_1']
                address.line_2 = registration_form.cleaned_data['line_2']
                address.city = registration_form.cleaned_data['city']
                address.county = registration_form.cleaned_data['county']
                address.postcode = registration_form.cleaned_data['postcode']
                address.user = user
                address.save()

                messages.info(request, "Congratulations, you have successfully registered with Pleasures All Mine.")
                send_welcome_email(user_profile.user)
                user = authenticate(
                    username=registration_form.cleaned_data['email'],
                    password=registration_form.cleaned_data['password']
                )
                login_after_registration(request, user)
                return HttpResponseRedirect(next_url)
            else:
                registration_form = RegistrationForm(data=request.POST)
                messages.warning(request, "Sorry, but you missed something, please fill all required fields.")

        if 'login' in request.POST:
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = authenticate(username=login_form.cleaned_data['username'],
                        password=login_form.cleaned_data['password'])
                if user is not None:
                    if not request.POST.get('remember_me', None):
                        request.session.set_expiry(0)
                    messages.success(request, "Welcome to Pleasures All Mine, you have successfully logged in.")
                    return login(request, authentication_form=LoginForm,)
                else:
                    login_form = LoginForm()
                    registration_form = RegistrationForm()
                    messages.warning(request, "Sorry, but you missed something, please fill all required fields.")
            else:
                messages.warning(request, "Sorry, but the username or password you have entered is incorrect, please try again.")
                login_form = LoginForm()
                registration_form = RegistrationForm()
        else:
            login_form = LoginForm()
    else:
        registration_form = RegistrationForm()
        login_form = LoginForm()
    return render_to_response(
            'accounts/login_register.html',
            {
                'registration_form': registration_form,
                'login_form': login_form,
                'message': message,
                'next_url': next_url,
                }, RequestContext(request) )

def thank_you(request):

    return render_to_response('accounts/thank_you.html', context_instance=RequestContext(request))

def edit_customer(request, profile_id):
    if profile_id is not None:
        user_profile = get_object_or_404(UserProfile, pk=profile_id)
        user = user_profile.user
        try:
            address = Address.objects.get(user=user)
        except Address.DoesNotExist:
            address = None
        if request.POST:
            userprofile_form = UserProfileForm(request.POST,)
            if userprofile_form.is_valid():
                user_profile.title = userprofile_form.cleaned_data['title']
                user_profile.date_of_birth = userprofile_form.cleaned_data['date_of_birth']
                user_profile.phone = userprofile_form.cleaned_data['phone']

                user_profile.save()

            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                if not address:
                    address = Address()
                    address.user = user
                address.line_1 = address_form.cleaned_data['line_1']
                address.line_2 = address_form.cleaned_data['line_2']
                address.city = address_form.cleaned_data['city']
                address.county = address_form.cleaned_data['county']
                address.postcode = address_form.cleaned_data['postcode']
                address.save()

        return render_to_response('admin/accounts/edit_customer.html',
                {
                    'userprofile_form': UserProfileForm(instance=user_profile),
                    'address_form': AddressForm(instance=address),
                    'user_profile' : user_profile,
                },   RequestContext(request)
                )
def logout_view(request):
    logout(request)
    messages.warning(request, "Thank you for shopping with Pleasures All Mine, you have successfully logged out.")
    return HttpResponseRedirect('/')


@transaction.commit_on_success
def add_customer(request):
    form = RegistrationFormAdmin()
    if request.method == "POST":
        form = RegistrationFormAdmin(request.POST)
        if form.is_valid():
            username = generate_username(form.cleaned_data['first_name'],
                                         form.cleaned_data['last_name'],
            )
            random_password = get_pronounceable_password()
            user = User.objects.create_user(
                    username,
                    form.cleaned_data['email'],
                    random_password
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active = True
            user.save()

            userprofile = UserProfile()
            userprofile.title = form.cleaned_data['title']
            userprofile.date_of_birth = form.cleaned_data['date_of_birth']
            userprofile.phone = form.cleaned_data['phone']
            userprofile.terms = form.cleaned_data['terms']
            userprofile.user = user
            userprofile.save()

            address = Address()
            address.line_1 = form.cleaned_data['line_1']
            address.line_2 = form.cleaned_data['line_2']
            address.city = form.cleaned_data['city']
            address.county = form.cleaned_data['county']
            address.postcode = form.cleaned_data['postcode']
            address.user = user
            address.save()

            send_admin_welcome_email(user, random_password)
            return HttpResponseRedirect('/admin/accounts/userprofile/')

        else:
            form = RegistrationFormAdmin(request.POST)

    return render_to_response('admin/accounts/add_customer.html',
            {'form': form}, context_instance=RequestContext(request))
