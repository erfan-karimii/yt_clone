from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
import random
from .forms import EmailForm , ProfileForm
from .models import Profile
# Create your views here.

MyUser = get_user_model()

def registerView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form=EmailForm(request.POST)
        if form.is_valid():
            number = random.randint(1000, 99999)
            email =form.cleaned_data['email']
            if MyUser.objects.filter(email=email):
                MyUser.objects.filter(email=email).update(token=number)
            else:
                MyUser.objects.create(email=email,token=number)
            # send email code
            print(number)
            response = render(request,'account/verify.html')
            
            response.set_cookie('email_cookie',email,1000)
            return response
        else:
            messages.error(request,'ایمیل خود را درست وارد کنید')
            return redirect('account:registerView')
    else :
        return render(request,'account/register.html',{})

def VerifyChecked(request):
    if request.method == "POST":
        try :
            email_c = request.COOKIES['email_cookie']
            user = MyUser.objects.get(email=email_c)
        except KeyError:
            messages.error(request,'زمان احراز هویت شما به پایان رسیده است ')
            return redirect('account:registerView')
        token = request.POST.get('token')
        if user.token == token :
            MyUser.objects.filter(email=email_c).update(is_verified=True)
            return redirect('account:set_password')
        else :
            messages.error(request,'کدارسالی را درست وارد کنید')
            return redirect('account:verify')
    return render(request,'account/verify.html')

def set_password(request):
    if request.method == "POST":
        try:
            email = request.COOKIES['email_cookie']
        except KeyError:
            messages.error(request,'زمان احراز هویت شما به پایان رسیده است ')
            return redirect('account:registerView')
        password = request.POST.get('password')
        MyUser.objects.filter(email=email).update(
            password=make_password(password)
        )
        user = MyUser.objects.get(email=email)
        messages.success(request,'پسورد شما با موفقست ثبت شد.')
        if user.is_verified:
            login(request, user)
            return redirect('/')
    elif request.method == "GET":
        return render(request,'account/setpassword.html',{})

@login_required(login_url='/accounts/login/')
def ComplateProfile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'پروفایل شما با ویرایش  شد')
        else:
            print(form.errors)
            messages.error(request,'لطفا با دقت همه فیلد هارا پرکنید')
    form = ProfileForm(instance=profile)
    return render(request,'account/completeprofile.html',{'profile':profile,'form':form})

def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_verified:
                login(request, user)
                messages.success(request,'شما با موفقیت وارد حساب کاربری خود شدید')
                print(request.GET)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('/')
            else:
                messages.error(request,"شما احراز هویت نشده ایید")
        else:
            messages.error(request,'ایمیل یا رمز عبور اشتباه است')
    form = AuthenticationForm()
    return render(request,'account/login.html',{'form':form})

def LogOut(request):
    logout(request)
    messages.success(request,"شما با موفقیت از حساب کاربری خود خارج شدید")
    return redirect('/')
