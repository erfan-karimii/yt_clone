from django.shortcuts import render ,redirect
from account.models import Profile
from django.contrib import messages
from .models import Video
from .forms import VideoEditForm
# Create your views here.

def index(request):
    context = {
        'latest_videos': Video.objects.filter(published=True).order_by('-created'),
    }
    return render(request,'index.html',context)

def upload_video(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        video = request.FILES.get('video')
        Video.objects.create(youtuber=profile,video=video)
        messages.success(request,'ویدیو شما در یافت شد و در حال اپلود می باشد.')
    return render(request,'upload_video.html',{})

def upload_list(request):
    profile = Profile.objects.get(user=request.user)
    videos = Video.objects.filter(youtuber=profile)
    context = {
        'videos' : videos,
    }
    return render(request,'upload_list.html',context)

def upload_edit(request,id):
    video = Video.objects.get(id=id)
    if request.method == 'POST':
        print(request.POST)
        form = VideoEditForm(request.POST,request.FILES,instance=video)
        if form.is_valid():
            video = form.save()
            video.published = True
            video.save()
            messages.success(request,'ویدیو شما با موفقیت ادیت شد.')
        else:
            print(form.errors)
            messages.error(request,'.لطفا همه فیلد رو با دقت کامل کنید')
    else:
        form = VideoEditForm(instance=video)
    
    context = {
        'form' : form,
        'video' : video, 
    }
    return render(request,'upload_edit.html',context)

def upload_delete(request,id):
    profile = Profile.objects.get(user=request.user)
    video = Video.objects.get(id=id,youtuber=profile)
    video.delete()
    messages.success(request,'ویدیو شما حذف شد.')
    return redirect('youtube:upload_list')

def video_detail(request,id):
    video = Video.objects.get(id=id,published=True)
    context = {
        'video' : video,
    }
    return render(request,'video_detail.html',context)
