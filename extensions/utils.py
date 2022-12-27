from django.utils import timezone
from . import jalali

def convert_to_persian_number(eng_string):
    nums = (
        '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰'
    )
    
    for eng, ir in enumerate(nums):
        ir_string = eng_string.replace(str(eng), ir)
    
    return ir_string

def convert_to_jalali(time):
    jmonths = (
        'فروردین',
        'اردیبهشت',
        'خرداد',
        'تیر',
        'مرداد',
        'شهریور',
        'مهر',
        'آبان',
        'آذر',
        'دی',
        'بهمن',
        'اسفند'
    )
    
    time = timezone.localtime(time)
    time_to_str = f'{time.year},{time.month},{time.day}'
    time_to_list = list(jalali.Gregorian(time_to_str).persian_tuple())
    
    for i, month in enumerate(jmonths):
        if time_to_list[1] == i + 1:
            time_to_list[1] = month
            break
    
    jalali_time = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}, ساعت: {time.hour}:{time.minute}'

    return convert_to_persian_number(jalali_time)