from django import template

register = template.Library()


# @register.filter(name='days_passed') 
# def days_passed(date):
#     today = datetime.now(timezone.utc)
#     days_passed = today - date
#     return f"{days_passed.days} روز پیش" if days_passed.days != 0 else 'امروز'
