import datetime
import os
from io import BytesIO
from os.path import join, isfile, isdir

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UploadFileForm, UploadIconModelForm
from .models import UploadIcons
from .utility import make_thumbnail, sizeof_fmt


def home(request):
    if request.method == 'GET':
        action = request.GET.get('do')
        if action == 'del':
            try:
                image_id = request.GET.get('id')
                # print('id: %s' % image_id)
                obj = UploadIcons.objects.get(pk=image_id)
                # print(obj)
                image_title = obj.Title
                # print(image_title)
                obj.delete()
                message = "\033[93m*** 圖片 [%s] 已被刪除.\033[00m" % image_title
                print(message)
                return redirect(reverse('fileupload:home'))
            except Exception as e:
                message = 'Can not fine the image ! (No file has been delete.)'
        elif action == 'del_file':
            file_name = request.GET.get('file')
            folder = settings.MEDIA_ROOT + '/upload/'
            full_path = join(folder, file_name)
            try:
                os.remove(full_path)
                message = "\033[93m*** 圖片 [%s] 已被刪除.\033[00m" % file_name
                print(message)
                return redirect(reverse('fileupload:home'))
            except Exception as e:
                message = 'Can not fine the image ! (No file has been delete.)'

    upload_path = settings.MEDIA_ROOT + '/upload/'
    # print('Path: %s' % upload_path)
    if os.path.exists(upload_path.strip().replace('?', '')):
        # print('***目錄已存在')
        pass
    else:
        os.makedirs(upload_path.strip().replace('?', ''))
        print('\033[93m*** 目錄不存在，建立目錄\033[00m')
    # 取得所有檔案與子目錄名稱
    files = os.listdir(upload_path)
    # print('The files in the folder: %s' % files)
    # 以迴圈處理
    image_path = settings.MEDIA_URL + 'upload/'
    images_list = []
    for file in files:
        # 產生檔案的絕對路徑
        fullpath = join(upload_path, file)
        # 判斷 fullpath 是檔案還是目錄
        if isfile(fullpath):
            images_list.append({'file': file, 'path': image_path + file})
            # print("檔案:", file, " 路徑：", fullpath)
        elif isdir(fullpath):
            print("目錄：", file)
    icons = UploadIcons.objects.all()
    upload_form = UploadFileForm
    icon_form = UploadIconModelForm
    return render(request, 'fileupload/home.html', locals())


def save_to_file(request):
    # Direct Save to file.
    if request.method == 'POST':
        receive_form = UploadFileForm(request.POST, request.FILES)
        receive_file = request.FILES['file']
        if receive_form.is_valid():
            # print(type(receive_file))
            # print('The size of file is %d bytes' % receive_file.size)
            now_time = datetime.datetime.now()
            # 避免相同檔名覆蓋
            new_file_name = now_time.strftime('%Y%m%d_%H%M%S' + '.jpg')
            # print('File Name is %s' % new_file_name)
            message = '\033[93m*** 圖片 [%s] 已經儲存為 [%s].\033[00m' % (receive_file, new_file_name)
            store_path = settings.MEDIA_ROOT + '/upload/'
            # print('Path: %s' % path_file)
            # 將上傳的資料儲存於記憶體
            file_string = BytesIO()
            for part in receive_file.chunks():
                file_string.write(part)
                file_string.flush()

            file_name = receive_file.name
            image_file = make_thumbnail(file_string, file_name, size=(800, 800))
            fs = FileSystemStorage()
            fs.save(store_path + new_file_name, image_file)
            print(message)
    return redirect(reverse('fileupload:home'))


def save_to_model(request):
    if request.method == 'POST':
        receive_form = UploadIconModelForm(request.POST, request.FILES)
        icon_title = request.POST.get('Title')
        icon_description = request.POST.get('Description')
        # print(icon_title)
        capt = request.POST.get("captcha_1", None)  # User Key In
        key = request.POST.get("captcha_0", None)  # Database store

        if icon_title is not None:
            # Reduce image size
            post_image = request.FILES.get('IconImage')
            message = '\033[93m*** 圖片 [%s] 已經儲存.\033[00m' % icon_title
            file_string = BytesIO()
            for part in post_image.chunks():  # 將上傳的資料儲存於記憶體
                file_string.write(part)
                file_string.flush()

            file_name = post_image.name
            image = make_thumbnail(file_string, file_name, size=(800, 800))

            try:
                new_image = UploadIcons.objects.create()
                new_image.Title = icon_title
                new_image.Description = icon_description
                new_image.IconImage = image
                # print('Save')
                new_image.save()
                print(message)

            except Exception as e:
                message = 'The error: %s' % e
                print(message)
        else:
            icons = UploadIcons.objects.all()
            upload_form = UploadFileForm
            icon_form = UploadIconModelForm
            message = '檔案不存在！'
        return redirect(reverse('fileupload:home'))


# Update the model data or image.
def update(request, image_id):
    print('\033[93m*** Update Image ID:%s\033[00m' % image_id)
    pick_data = get_object_or_404(UploadIcons, pk=image_id)
    title = request.POST.get('update_title')
    description = request.POST.get('update_description')
    image_file = request.FILES.get('update_image')
    pick_data.Title = title
    pick_data.Description = description
    if image_file is not None:
        file_string = BytesIO()
        for part in image_file.chunks():  # 將上傳的資料儲存於記憶體
            file_string.write(part)
            file_string.flush()

        file_name = image_file.name
        new_image = make_thumbnail(file_string, file_name, size=(800, 800))
        pick_data.IconImage = new_image
    else:
        pass
    # print(image_id)
    # print(title)
    # print(image_file)
    print('\033[93m*** 圖片[%s]已更新:\033[00m' % pick_data.Title)
    pick_data.save()
    return redirect(reverse('fileupload:home'))


# 刪除使用 FileField 或是 ImageField 儲存的檔案, Delete real image when model do delete data.
@receiver(post_delete, sender=UploadIcons)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.IconImage.delete(save=False)
    except Exception as e:
        print("Error: %s" % e)


# 更新使用 FileField 或是 ImageField 儲存的檔案, Check New image exist, Delete Old Image or not.
@receiver(pre_save, sender=UploadIcons)
def pre_save_image(sender, instance, *args, **kwargs):
    """ If instance is old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).IconImage.path
        try:
            new_img = instance.IconImage.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except Exception as e:
        print("Error: %s" % e)
