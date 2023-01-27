# Files-Upload-Demo
The Project is show how to manage upload files with Django.  
***
Free for personal use.  
Please contact me for Business use.
***

If you want to use Pillow in Termux,

You should install the library first for image handling.
```commandline
pkg install libjpeg-turbo
```

### Install method:  
```
git clone https://github.com/miniCloudMES/Upload_Demo.git 
cd Upload_Demo/mainsite 
pip install -r requirements.txt  
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
If you want to share the web for other device with local network.  
Check your phone IP with:
```commandline
ifconfig
```
Start Up server with:
```commandline
python manage.py runserver 0.0.0.0:8000
```