from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
from django.http import HttpResponse
import re
from Add_Data.models import Disease , AnalysisImage , PrescriptionImage
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        city = request.POST.get('city')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        doctor = 'is_doctor' in request.POST
        description = request.POST.get('description') if doctor else ''
        degree_certificate = request.FILES.get('degree_certificate') if doctor else None
        syndicate_card = request.FILES.get('syndicate_card') if doctor else None
        terms = request.POST.get('terms')

        if all([firstname, lastname, username, password, phone, email, city, age, gender]):
            if terms:
                if User.objects.filter(username=username).exists():
                    return HttpResponse('Sorry, this username is taken')
                elif User.objects.filter(email=email).exists():
                    return HttpResponse('Sorry, this email is taken')
                else:
                    email_pattern = r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                    if re.match(email_pattern, email):
                        user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                        user.save()
                        userprofile = UserProfile(
                            user=user, 
                            phone=phone, 
                            city=city, 
                            age=age, 
                            gender=gender, 
                            is_doctor=doctor
                        )
                        if doctor:
                            userprofile.description = description
                            userprofile.degree_certificate = degree_certificate
                            userprofile.syndicate_card = syndicate_card
                        userprofile.save()
                        return redirect('signin')
                    else:
                        return HttpResponse('Sorry, there was an error with your email format')
            else:
                return HttpResponse('Sorry, you must agree to the terms')
        else:
            return HttpResponse('Sorry, you have not filled in all the required fields')
    else:
        return render(request, 'accounts/signup.html')


def signin(request):
    if request.method == 'POST' and 'btnsignin' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        is_doctor = request.POST.get('is_doctor') == 'on'

        # Print entered values for verification
        print(f"Username: {username}, Password: {password}, Is Doctor: {is_doctor}")

        # Check the validity of username and password
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            print(f"Authenticated user: {user.username}")
            try:
                user_profile = UserProfile.objects.get(user=user)
                print(f"User profile found for: {user.username}, Is Doctor: {user_profile.is_doctor}")
                if is_doctor and not user_profile.is_doctor:
                    messages.error(request,'You are not authorized as a doctor')
                    return render(request, 'accounts/signin.html')
            except UserProfile.DoesNotExist:
                print(f"No user profile found for: {user.username}")
                return HttpResponse('User profile not found')

            auth.login(request, user)
            return render(request, 'pages/home.html')
        else:
            print(f"Invalid login for user: {username}")
            return HttpResponse('You entered an invalid username or password')
    else:
        return render(request, 'accounts/signin.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('homeback')
    else:
        return HttpResponse('You are not logged in to the website.')

def account(request):
    if request.method == 'POST' and 'btnsave' in request.POST:
        # حفظ التغييرات
        if request.user is not None and request.user.id is not None:
            userprofile = UserProfile.objects.get(user=request.user)

            if all([request.POST['firstname'], request.POST['lastname'], request.POST['username'], request.POST['password'], request.POST['phone'], request.POST['email'], request.POST['city'], request.POST['gender'], request.POST['age']]):
                request.user.first_name = request.POST['firstname']
                request.user.last_name = request.POST['lastname']
                #request.user.username = request.POST['username']
                if not request.POST['password'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['password'])
                
                userprofile.phone = request.POST['phone']
                #request.user.email = request.POST['email']
                userprofile.city = request.POST['city']
                userprofile.gender = request.POST['gender']
                userprofile.age = request.POST['age']
                #userprofile.description = request.POST['description']
                
                request.user.save()
                userprofile.save()
            else:
                return HttpResponse('تحقق من قيم الحقول والعناصر')
        return redirect('account')
    else:
        if request.user is not None:
            context = None
            if not request.user.is_anonymous:
                userprofile = UserProfile.objects.get(user=request.user)
                context = {
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,
                    'user': request.user.username,
                    'password': request.user.password,
                    'phone': userprofile.phone,
                    'email': request.user.email,
                    'city': userprofile.city,
                    'gender': userprofile.gender,
                    'age': userprofile.age,
                    'description': userprofile.description,
                    'degree_certificate': userprofile.degree_certificate.url if userprofile.degree_certificate else None,
                    'syndicate_card': userprofile.syndicate_card.url if userprofile.syndicate_card else None,
                }
                
            return render(request, 'accounts/account.html', context)
        else:
            return redirect('signin')



def forget_reset_pass(request):
    if request.method == 'POST':
        if 'btnforgetpass' in request.POST:
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                reset_code = get_random_string(length=6, allowed_chars='0123456789')
                user.userprofile.reset_code = reset_code
                user.userprofile.save()
                send_mail(
                    'Password Reset Code',
                    f'Your password reset code is {reset_code}',
                    email,  # استخدام بريد المستخدم الإلكتروني كمرسل
                    [email],
                    fail_silently=False,
                )
                return render(request, 'accounts/forget_reset_pass.html', {'stage': 'reset', 'email': email})
            except User.DoesNotExist:
                return HttpResponse('This email is not registered.')

        elif 'btnresetpass' in request.POST:
            email = request.POST['email']
            reset_code = request.POST['reset_code']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if new_password != confirm_password:
                return HttpResponse('Passwords do not match.')

            try:
                user = User.objects.get(email=email)
                if user.userprofile.reset_code == reset_code:
                    user.set_password(new_password)
                    user.userprofile.reset_code = None
                    user.save()
                    user.userprofile.save()
                    return redirect('signin')
                else:
                    return HttpResponse('Invalid reset code.')
            except User.DoesNotExist:
                return HttpResponse('This email is not registered.')

    return render(request, 'accounts/forget_reset_pass.html', {'stage': 'forget'})



@login_required
def search(request):
    diseases_list = Disease.objects.filter(patient=request.user)
    disease = None

    if 'username' in request.GET:
        username = request.GET['username']
        if username:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                return render(request, 'accounts/search.html', {'user_found': False, 'error_message': 'User profile not found'})

            if user_profile.is_doctor:
                # The user is a doctor and is searching for a patient
                try:
                    patient_profile = UserProfile.objects.get(user__username=username, is_doctor=False)
                    diseases_list = Disease.objects.filter(patient=patient_profile.user)  # Fetch diseases of the patient
                    context = {
                        'user_found': True,
                        'patient_profile': patient_profile,
                        'diseases_list': diseases_list,
                    }
                    if 'disease_name' in request.GET and request.GET['disease_name']:
                        disease_name = request.GET['disease_name']
                        disease = diseases_list.filter(disease_name=disease_name).first()
                        if disease:
                            context['disease'] = disease
                            context['disease_details'] = {
                                'disease_name': disease.disease_name,
                                'analysis_images': AnalysisImage.objects.filter(disease=disease),
                                'prescription_images': PrescriptionImage.objects.filter(disease=disease),
                                'modified_dates': disease.modified_dates.split(",") if disease.modified_dates else []
                            }
                    return render(request, 'accounts/search.html', context)
                except UserProfile.DoesNotExist:
                    error_message = 'Patient not found'
            else:
                # The user is a patient and is searching for a doctor
                try:
                    doctor_profile = UserProfile.objects.get(user__username=username, is_doctor=True)
                    context = {
                        'user_found': True,
                        'doctor_profile': doctor_profile,
                        'diseases_list': diseases_list,
                    }
                    return render(request, 'accounts/search.html', context)
                except UserProfile.DoesNotExist:
                    error_message = 'Doctor not found'
        else:
            error_message = 'Please provide a username'

        context = {'user_found': False, 'error_message': error_message}
        return render(request, 'accounts/search.html', context)
    else:
        return render(request, 'accounts/search.html')

from django.core.mail import send_mail
from .forms import ContactForm

def contact_view(request):
    success_message = None
    if request.method == 'GET':
        form = ContactForm(request.POST)
        if form.is_valid():
            # استخراج البيانات
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # إرسال البريد (يمكن تخصيصه حسب الحاجة)
            send_mail(
                subject=f"Contact Us: {subject}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                fail_silently=False,
            )
            success_message = "Thank you for contacting us. We will get back to you soon."
            form = ContactForm()  # إعادة تعيين النموذج بعد الإرسال
    else:
        form = ContactForm()
    return render(request, 'accounts/contact_us.html', {'form': form, 'success_message': success_message})
