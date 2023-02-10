from django.shortcuts import render
from .models import NavOne
from account.models import Profile
# Create your views here.
def header_view(request):
    profile = ''
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        
    context = {
        'navones':NavOne.objects.all(),
        'profile':profile,

    }
    return render(request,'layout/header.html',context)