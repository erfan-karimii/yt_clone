from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.db.models import Count , Q
from django.contrib.auth.decorators import login_required
from pytube import YouTube
from account.models import Profile
from .models import Video , VideoTag , PlayList , Category
from .forms import VideoEditForm
# Create your views here.

def index(request):
    videos = Video.objects.all_video().order_by('-created')
    channels = Profile.objects.exclude(image='').annotate(most_like=Count('video__like')).exclude(most_like=0).order_by('-most_like')
    favorite_videos = Video.objects.all_video().annotate(like_count=Count('like')).order_by('-like_count','-created')
    categorys = Category.objects.all()
    context = {
        'latest_videos': videos,
        'channels' : channels,
        'favorite_videos' : favorite_videos,
        'categorys' : categorys,
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

def upload_video_from_yotube(request):
    if request.method == 'POST':
        link = request.POST.get('yt_link')
        video = YouTube(link)
        


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
    profile = Profile.objects.filter(user=request.user).first()
    
    if video.youtuber in profile.follow.all():
        is_followed = True
    else :
        is_followed = False
    
    ids=video.tags.values_list('id',flat=True)
    similar_videos = Video.objects.all_video(tags__in=ids).exclude(id=id)
    similar_videos = similar_videos.annotate(s_count=Count('tags')).order_by('-s_count','-created')[:6]

    hit_count = get_hitcount_model().objects.get_for_object(video)
    hits = hit_count.hits
    hitcontext = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    
    context = {
        'video' : video, 
        'is_followed' : is_followed,
        'similar_videos': similar_videos,
    }

    return render(request,'video_detail.html',context)

def add_new_tag_ajax(request):
    tag_name = request.GET.get('tag_name')
    tag = VideoTag.objects.create(name=tag_name)
    return JsonResponse({'id':tag.id})

def like_video_ajax(request):
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    profile = Profile.objects.get(user=request.user)
    if profile in video.like.all():
        video.like.remove(profile)
        status = 'removed'
    else:
        video.like.add(profile)
        status = 'added'
    return JsonResponse({'status':status})

def follow_channel_ajax(request):
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
    return JsonResponse({'status':status})

def watch_later_ajax(request):
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    profile = Profile.objects.get(user=request.user)
    playlist = PlayList.objects.get(profile=profile,name='watch_later')
    if video in playlist.video.all():
        playlist.video.remove(video)
        status = 'removed'
    else : 
        playlist.video.add(video)
        status= 'added'
    return JsonResponse({'status':status})

def get_playlist_ajax(request):
    profile = Profile.objects.get(user=request.user)
    playlists = PlayList.objects.filter(profile=profile).exclude(name='watch_later').values_list('name',flat=True)
    return JsonResponse({'playlists':list(playlists)})

def add_video_to_playlist_ajax(request):
    playlist_name = request.GET.get('playlist_name')
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    playlist = PlayList.objects.get(name=playlist_name)
    if video in playlist.video.all():
        playlist.video.remove(video)
        status = 'removed'
    else :
        playlist.video.add(video)
        status = 'added'
    return JsonResponse({'status':status})

def create_playlist_ajax(request):
    profile = Profile.objects.get(user=request.user)
    playlist_name = request.GET.get('playlist_name')
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    obj,created = PlayList.objects.get_or_create(name=playlist_name,defaults={'profile':profile,})

    if created:
        obj.video.add(video)
        status = 'play list created and video added'
    else:
        status = 'this play list already exists'
    return JsonResponse({'status':status})

def delete_playlist(request,id):
    profile = Profile.objects.get(user=request.user)
    playlist = PlayList.objects.get(~Q(name='watch_later'),id=id,profile=profile)
    playlist.delete()
    messages.success(request,'پلی لیست با موفقیت حذف شد')
    return redirect('youtube:channel_home_page',id=profile.id)

def channel_home_page(request,id):
    yt_profile = get_object_or_404(Profile,id=id)
    order_by = request.GET.get('orderby')
    if order_by:
        all_video = yt_profile.video_set.filter(published=True).order_by(order_by)
    else :
        all_video = yt_profile.video_set.filter(published=True).order_by('-created')
    play_lists = PlayList.objects.filter(profile=yt_profile)
    
    is_followed = False
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if yt_profile in profile.follow.all():
            is_followed = True

    context = {
        'yt_profile' : yt_profile,
        'videos' : all_video,
        'is_followed' : is_followed,
        'play_lists' : play_lists,
        'order_by' : order_by,
    }
    return render(request,'channel_home_page.html',context)
