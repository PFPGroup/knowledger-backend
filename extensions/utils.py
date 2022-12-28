from django.apps import apps
from django.utils import timezone
from . import jalali
from django.core.files import File
from PIL import Image
from io import BytesIO


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

def image_name_create(username, type):
    persian_time = convert_to_jalali(timezone.now())
    name = f'{username}-{persian_time}.{type}'
    return name

def compress_image(image, username):
    if 'default_shelve' in image.name or 'default_book' in image.name:
        return image

    img = Image.open(image)
    img_io = BytesIO() 
    if img.mode == 'RGBA':
        img.save(img_io, 'PNG', quality=70, optimize=True) 
        name=image_name_create(username, type='PNG')
    else:
        img.save(img_io, 'JPEG', quality=70, optimize=True)
        name=image_name_create(username, type='JPEG')

    new_image = File(img_io, name=name)
    return new_image

def create_thumbnail(image, username, size=(240, 240)):
    if 'default_shelve' in image.name or 'default_book' in image.name:
        return image

    img = Image.open(image)
    img.thumbnail(size)
    thumb_io = BytesIO() 
    
    if img.mode == 'RGBA':
        img.save(thumb_io, 'PNG', quality=70, optimize=True) 
        name=image_name_create(username, type='PNG')
    else:
        img.save(thumb_io, 'JPEG', quality=70, optimize=True)
        name=image_name_create(username, type='JPEG')
    thumbnail = File(thumb_io, name=name)
    return thumbnail


def check_client_ip(instance, ip):
    BookViews = apps.get_model('bookstack.BookViews')
    ip_obj, created = BookViews.objects.get_or_create(ip_address=ip)
    if created:
        instance.ip.add(ip_obj)
        instance.views_count += 1
        instance.save()
    return None