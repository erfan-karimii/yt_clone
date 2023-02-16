from django.shortcuts import render ,redirect
from account.models import Profile
from django.contrib import messages
from django.http import JsonResponse
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from .models import Video , VideoTag
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
    context = {}

    hit_count = get_hitcount_model().objects.get_for_object(video)
    hits = hit_count.hits
    hitcontext = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    
    context['video'] = video
    return render(request,'video_detail.html',context)

def add_new_tag_ajax(request):
    tag_name = request.GET.get('tag_name')
    tag = VideoTag.objects.create(name=tag_name)
    return JsonResponse({'id':tag.id})

def like_video_ajax(request):
    if request.user.is_authenticated:
        video_id = request.GET.get('video_id')
        profile = Profile.objects.get(user=request.user)
        video = Video.objects.get(id=video_id)
        if profile in video.like.all():
            video.like.remove(profile)
            status = 'removed'
        else:
            video.like.add(profile)
            status = 'added'
    else :
        status = 'fail' 
    return JsonResponse({'status':status})
