from django import template
from datetime import datetime , timezone , timedelta
from youtube.models import Category
register = template.Library()


@register.filter(name='history_video_days_passed') 
def history_video_days_passed(date):
    today = datetime.now(timezone.utc)
    days_passed = today - date
    return f"{days_passed.days} روز پیش" if days_passed.days != 0 else f'{timedelta(seconds=int(days_passed.seconds))} قبل '

@register.simple_tag(name='count_category_video') 
def count_category_video(cat_id):
    category = Category.objects.get(id=cat_id)
    video_count = category.video_set.filter(published=True).count()
    return video_count