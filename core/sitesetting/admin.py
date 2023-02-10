from django.contrib import admin
from .models import SiteSetting,NavOne,NavTwo,FooterOne,FooterTwo
# Register your models here.


admin.site.register(SiteSetting)
admin.site.register(NavOne)
admin.site.register(NavTwo)
admin.site.register(FooterOne)
admin.site.register(FooterTwo)

