from django.urls import path
from . import views


app_name='account'

urlpatterns = [
    path("register/",views.registerView,name='registerView'),
    path('VerifyChecked/',views.VerifyChecked,name='verify'),
    path('set_password/',views.set_password,name='set_password'),
    path('complateprofile/',views.ComplateProfile,name='complate'),

    path('accounts/login/',views.Login,name='login'),
    path('logout/',views.LogOut,name='logout'),
]


