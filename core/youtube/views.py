from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from account.models import Profile
from .models import Video , VideoTag , PlayList
from .forms import VideoEditForm
# Create your views here.

def index(request):
    videos = Video.objects.all_video().order_by('-created')
    channels = Profile.objects.exclude(image='').annotate(most_like=Count('video__like')).exclude(most_like=0).order_by('-most_like')
    favorite_videos = Video.objects.all_video().annotate(like_count=Count('like')).order_by('-like_count','created')
    context = {
        'latest_videos': videos,
        'channels' : channels,
        'favorite_videos' : favorite_videos,
    }
    return render(request,'index.html',context)

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def video_detail(request,id):
    video = Video.objects.get(id=id,published=True)
    user_profile = Profile.objects.filter(user=request.user).first()
    if video.youtuber in user_profile.follow.all():
        is_followed = True
    else :
        is_followed = False
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
    context['is_followed'] = is_followed
    return render(request,'video_detail.html',context)

def add_new_tag_ajax(request):
    tag_name = request.GET.get('tag_name')
    tag = VideoTag.objects.create(name=tag_name)
    return JsonResponse({'id':tag.id})

def like_video_ajax(request):
    if request.user.is_authenticated:
        video_id = request.GET.get('video_id')
        video = Video.objects.get(id=video_id)
        profile = Profile.objects.get(user=request.user)
        if profile in video.like.all():
            video.like.remove(profile)
            status = 'removed'
        else:
            video.like.add(profile)
            status = 'added'
    else :
        status = 'fail' 
    return JsonResponse({'status':status})

def follow_channel_ajax(request):
    if request.user.is_authenticated:
        yt_user = request.GET.get('yt_user')
        yt_profile= Profile.objects.get(user=yt_user)
        profile = Profile.objects.get(user=request.user)
        if yt_profile == profile:
            status = 'same'
        elif yt_profile in profile.follow.all():
            profile.follow.remove(yt_profile)
            status = 'removed'
        else:
            profile.follow.add(yt_profile)
            status = 'added'
    else:
        status = 'fail'
    return JsonResponse({'status':status})

def channel_home_page(request,id):
    profile = get_object_or_404(Profile,id=id)
    all_video = profile.video_set.filter(published=True).order_by('-created')
    play_lists = PlayList.objects.filter(profile=profile)

    user_profile = Profile.objects.filter(user=request.user).first()
    if profile in user_profile.follow.all():
        is_followed = True
    else :
        is_followed = False

    context = {
        'profile' : profile,
        'videos' : all_video,
        'is_followed' : is_followed,
        'play_lists' : play_lists,
    }
    return render(request,'channel_home_page.html',context)

