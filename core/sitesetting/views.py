from django.shortcuts import render , redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import NavOne ,FooterOne ,SiteSetting
from account.models import Profile
from . import tasks

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

class BucketHome(UserPassesTestMixin,View):
    template_name = 'bucket/bucket.html'
    def get(self,request):
        objects = tasks.all_bucket_objects_task()
        # for obj in objects:
        #     print(obj.__dir__())
        #     break
        return render(request,self.template_name,{'objects':objects})
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser
    
class DeleteBucketObject(UserPassesTestMixin,View):
    def get(self,request,key):
        tasks.delete_object_task.delay(key)
        messages.success(request,'your object will delete soon')
        return redirect('sitesetting:bucket')
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

class DownloadBucketObject(UserPassesTestMixin,View):
    def get(self,request,key):
        tasks.download_object_task.delay(key)
        messages.success(request,'your object will download soon')
        return redirect('sitesetting:bucket')
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

