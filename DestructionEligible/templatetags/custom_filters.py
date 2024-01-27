
from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='format_date_time')
def format_date_time(seconds):
    duration = timedelta(seconds=seconds)

    years = duration.days // 365
    months = (duration.days % 365) // 30
    days = duration.days % 30
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    formatted_time = ''
    
    if years:
        formatted_time += f"{years} {'year' if years == 1 else 'years'} "
    
    if hours:
        formatted_time += f"{hours} {'hour' if hours == 1 else 'hours'} "
    
    if minutes:
        formatted_time += f"{minutes} {'minute' if minutes == 1 else 'minutes'} "
    
    return formatted_time.strip()
