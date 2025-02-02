If you want to use uWsgi and nginx, you can install:
```commandline
pkg install uwgsi # Linux 
pip install uwgsi # Mac
pkg install nginx
```

Nginx 操作：  
優雅退出：nginx -s quit  
暴力退出： nginx -s stop  
重啟： nginx -s reload  
啟動： nginx  
啟動加上設置： nginx -c config.path  
測試設置參數： nginx -t -c config.path  
* Remark: config.path 表示 nginx.conf 的絕對路徑以及檔名 
* 查詢進程狀況：ps -ef | grep nginx


uwsgi 操作：  
啟動： uwsgi --ini ini.path  
停止： uwsgi --stop uwsgi.pid  
* Remark: ini.path 表示 uwsgi.ini 的路徑以及檔名  
* 查詢進程狀況：ps -ef | grep uwsgi

若上傳檔案出現：  
"/usr/local/var/run/nginx/client_body_temp/0000000001" failed (13: Permission denied)  
表示 client_body_temp/ 的權限沒有開放，請執行如下：  
```commandline
sudo chmod -R 775 client_body_temp
```