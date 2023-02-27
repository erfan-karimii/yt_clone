from django import template
from datetime import datetime , timezone , timedelta
register = template.Library()


@register.filter(name='history_video_days_passed') 
def history_video_days_passed(date):
    today = datetime.now(timezone.utc)
    days_passed = today - date
    return f"{days_passed.days} روز پیش" if days_passed.days != 0 else f'{timedelta(seconds=int(days_passed.seconds))} قبل '