from django.shortcuts import render
from .forms import VideoEditForm
# Create your views here.

def index(request):
    return render(request,'index.html',{})

def upload_video(request):
    return render(request,'upload_video.html',{})

def upload_edit(request):
    if request.method == 'POST':
        form = VideoEditForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
        else:
            print(form.errors)
    else:
        form = VideoEditForm()
    
    context = {
        'form' : form, 
    }
    return render(request,'upload_edit.html',context)