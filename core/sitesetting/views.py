from django.shortcuts import render
from django.views import View

from .models import NavOne ,FooterOne ,SiteSetting
from account.models import Profile
from .tasks import all_bucket_objects_task

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

class BucketHome(View):
    template_name = 'bucket/bucket.html'
    def get(self,request):
        objects = all_bucket_objects_task()
        return render(request,self.template_name,{'objects':objects})