from django.shortcuts import render
from .models import NavOne
# Create your views here.
def header_view(request):
    context = {
        'navones':NavOne.objects.all(),
    }
    return render(request,'layout/header.html',context)