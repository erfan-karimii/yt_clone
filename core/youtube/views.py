from django.shortcuts import render ,redirect ,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count , Q
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from urllib.error import URLError
import datetime

from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from hitcount.models import Hit
from pytube import YouTube
from pytube.exceptions import RegexMatchError , PytubeError

from account.models import Profile
from .models import Video , VideoTag , PlayList , Category , Comment
from .forms import VideoEditForm
from . import tasks
from time import sleep
# Create your views here.


def index(request):
    videos = Video.objects.all_video().order_by('-created')
    channels = Profile.objects.exclude(image='').annotate(most_like=Count('video__like')).exclude(most_like=0).order_by('-most_like')[0:4]
    favorite_videos = Video.objects.all_video().annotate(like_count=Count('like')).order_by('-like_count','-created')
    categorys = Category.objects.all()[0:4]
    context = {
        'latest_videos': videos,
        'channels' : channels,
        'favorite_videos' : favorite_videos,
        'categorys' : categorys,
    }
    return render(request,'index.html',context)

@login_required(login_url='/accounts/login/')
def upload_video(request):
    if request.method == 'POST':
        video = request.FILES.get('video')
        tasks.save_video_task.delay(str(video),str(video.temporary_file_path()),request.profile.id)
        sleep(5)
        messages.success(request,'ویدیو شما در یافت شد و در حال اپلود می باشد.')
        return redirect('/')
    return render(request,'upload_video.html',{})

@login_required(login_url='/accounts/login/')
def upload_list(request):
    # profile = Profile.objects.get(user=request.user)
    videos = Video.objects.filter(youtuber=request.profile)
    context = {
        'videos' : videos,
    }
    return render(request,'upload_list.html',context)

@login_required(login_url='/accounts/login/')
def upload_edit(request,id):
    video = Video.objects.get(id=id)
    if request.method == 'POST':
        form = VideoEditForm(request.POST,request.FILES,instance=video)
        if form.is_valid():
            video = form.save()
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

@login_required(login_url='/accounts/login/')
def upload_edit_youtube(request):
    url = request.GET.get('video-url')

    try :
        video = YouTube(url)
        title = video.title
        thumbnail_url = video.thumbnail_url
        length = datetime.timedelta(seconds=video.length).__str__()
        streams = video.streams.filter(file_extension='mp4').order_by('resolution')
        status = 'success'
    except RegexMatchError:
        status = 'url پیدا نشد!'
    except URLError:
        status = 'برای گرفتن ویدیو از یوتیوب متاسفانه باید از قندشکن استفاده کنید.' 
    except PytubeError:
        status = 'مشکلی پیش امده لطفا دوباره امتحان کنید.'
    
    if status != 'success':
        messages.error(request,status)
        return redirect('youtube:upload_video')
    
    context = {
        'form' : VideoEditForm(),
        'title' : title,
        'thumbnail_url':thumbnail_url,
        'length': length,
        'streams' : streams,
        'url':url,
    }
    return render(request,'upload_edit_youtube.html',context)

@login_required(login_url='/accounts/login/')
def save_video_from_youtube(request):
    itag = request.GET.get('itag')
    url = request.GET.get('url')
    tasks.save_video_from_youtube_task.delay(url,itag,request.profile.id)
    messages.success(request,'درخواست شما برای ذخیره ویدیو دریافت شد . به دلیل زمان \
    زیاد اپلود ان از یوتیوب به محض اتمام این فراید و برای ویرایش اطلاعات ویدیو برای شما ایمیل صادر خواهد شد')
    return redirect('youtube:home')

@login_required(login_url='/accounts/login/')
def upload_delete(request,id):
    video_obj = Video.objects.get(id=id,youtuber=request.profile)
    tasks.delete_video_with_object_task.delay(video_obj.video.name)
    video_obj.delete()
    messages.success(request,'ویدیو شما حذف شد.')
    return redirect('youtube:upload_list')

@login_required(login_url='/accounts/login/')
def video_detail(request,id):
    is_play_list = False
    play_list = []
    if request.GET.get('playlist'):
        is_play_list = True
        play_list = PlayList.objects.get(id=request.GET.get('playlist'))

    video = Video.objects.get(id=id,published=True)
    
    comments = Comment.objects.filter(video=video,is_show=True).order_by('-is_pin_comment','-created')
    
    is_followed = video.youtuber in request.profile.follow.all()
    
    ids=video.tags.values_list('id',flat=True)
    similar_videos = Video.objects.all_video(tags__in=ids).exclude(id=id)
    similar_videos = similar_videos.annotate(s_count=Count('tags')).order_by('-s_count','-created')[:6]

    hit_count = get_hitcount_model().objects.get_for_object(video)
    HitCountMixin.hit_count(request, hit_count)
    
    
    context = {
        'video' : video, 
        'is_followed' : is_followed,
        'similar_videos': similar_videos,
        'comments' : comments,
        'is_play_list' : is_play_list,
        'play_list' : play_list,
    }

    return render(request,'video_detail.html',context)

def add_new_tag_ajax(request):
    tag_name = request.GET.get('tag_name')
    tag = VideoTag.objects.create(name=tag_name)
    return JsonResponse({'id':tag.id})

def like_video_ajax(request):
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    # profile = Profile.objects.get(user=request.user)
    if request.profile in video.like.all():
        video.like.remove(request.profile)
        status = 'removed'
    else:
        video.like.add(request.profile)
        status = 'added'
    return JsonResponse({'status':status})

def follow_channel_ajax(request):
    yt_user = request.GET.get('yt_user')
    yt_profile= Profile.objects.get(user=yt_user)
    # profile = Profile.objects.get(user=request.user)
    if yt_profile == request.profile:
        status = 'same'
    elif yt_profile in request.profile.follow.all():
        request.profile.follow.remove(yt_profile)
        status = 'removed'
    else:
        request.profile.follow.add(yt_profile)
        status = 'added'
    return JsonResponse({'status':status})

def watch_later_ajax(request):
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    # profile = Profile.objects.get(user=request.user)
    playlist = PlayList.objects.get(profile=request.profile,name='watch_later')
    if video in playlist.video.all():
        playlist.video.remove(video)
        status = 'removed'
    else : 
        playlist.video.add(video)
        status= 'added'
    return JsonResponse({'status':status})

def get_playlist_ajax(request):
    # profile = Profile.objects.get(user=request.user)
    playlists = PlayList.objects.filter(profile=request.profile).exclude(name='watch_later').values_list('name',flat=True)
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
    # profile = Profile.objects.get(user=request.user)
    playlist_name = request.GET.get('playlist_name')
    video_id = request.GET.get('video_id')
    video = Video.objects.get(id=video_id)
    obj,created = PlayList.objects.get_or_create(name=playlist_name,defaults={'profile':request.profile,})

    if created:
        obj.video.add(video)
        status = 'play list created and video added'
    else:
        status = 'this play list already exists'
    return JsonResponse({'status':status})

def save_comment_ajax(request):
    body = request.GET.get('comment_body')
    if body :
        video_id = request.GET.get('video_id')
        video = Video.objects.get(id=video_id)
        try:
            Comment.objects.create(profile=request.profile,video=video,body=body)
            icon = 'success'
            status = 'کامنت شما ثبت شد و بعد از تایید ادمین نمایش داده می شود.'
        except IntegrityError:
            icon = 'error'
            status = 'شما مجاز به گذاشتن یک پیام بر روی هر ویدیو هستید.'
    else :
        icon = 'error'
        status = 'لطفا پیام بگذارید'
    return JsonResponse({'status':status,'icon':icon})

def delete_comment(request,id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    messages.success(request,'کامنت با موفقیت حذف شد.')
    prev =  request.GET.get('prev')
    return redirect(prev)

def pin_comment(request,id):
    comment = Comment.objects.get(id=id)
    if comment.is_pin_comment:
        comment.is_pin_comment = False
        comment.save()
        messages.success(request,'کامنت با موفقیت ان پین شد.')
    else :
        comment.is_pin_comment = True
        comment.save()
        messages.success(request,'کامنت با موفقیت پین شد.')
    prev =  request.GET.get('prev')
    return redirect(prev)

def delete_playlist(request,id):
    # profile = Profile.objects.get(user=request.user)
    playlist = PlayList.objects.get(~Q(name='watch_later'),id=id,profile=request.profile)
    playlist.delete()
    messages.success(request,'پلی لیست با موفقیت حذف شد')
    return redirect('youtube:channel_home_page',id=request.profile.id)

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
        if yt_profile in request.profile.follow.all():
            is_followed = True

    context = {
        'yt_profile' : yt_profile,
        'videos' : all_video,
        'is_followed' : is_followed,
        'play_lists' : play_lists,
        'order_by' : order_by,
    }
    return render(request,'channel_home_page.html',context)

def history_page(request):
    # historys_id = Hit.objects.filter(user=request.user).values_list('hitcount__object_pk',flat=True).order_by('-created')
    hits = Hit.objects.filter(user=request.user)
    # print(hits[0].hitcount.hit_count_generic_relation.all())
    # for y in hits :
    #     print(y.hitcount.hit_count_generic_relation.first().description)    

    return render(request,'history_page.html',{'hits':hits,})

def browse_category(request):
    categories = Category.objects.all()
    return render(request,'browse_categories.html',{'categories':categories})

def browse_channels(request):
    channels = Profile.objects.exclude(image='').annotate(most_like=Count('video__like')).exclude(most_like=0).order_by('-most_like')
    return render(request,'browse_channels.html',{'channels':channels})

def clear_watch_history(request):
    hits = Hit.objects.filter(user=request.user)
    if hits:
        hits.delete()
        messages.success(request,'تاریخچه شما با موفقیت پاک شد.')
    else:
        messages.error(request,'چیزی برای حذف کردن وجود ندارد.')
    return redirect('youtube:history_page')
