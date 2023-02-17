from django.shortcuts import render
from .models import NavOne ,FooterOne ,SiteSetting
from account.models import Profile
# Create your views here.
def header_view(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        
    context = {
        'navones':NavOne.objects.all(),
        'sitesetting' : SiteSetting.objects.last(), 
        'profile':profile,
    }
    return render(request,'layout/header.html',context)

def footer_view(request):
    context = {
        'footer_one' : FooterOne.objects.all(),
        'sitesetting' : SiteSetting.objects.last(), 
    }
    return render(request,'layout/footer.html',context)
