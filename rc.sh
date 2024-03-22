#!/bin/bash
mount -t ntfs-3g /dev/sda1 /mnt/SBC
#nohup /root/miniconda3/envs/py39/bin/gunicorn -c /root/SBCv2/gunicorn.py SBC.wsgi  -D &
#nohup gunicorn -c /root/SBCv2/gunicorn.py SBC.wsgi  -D &

#nginx
nohup /root/frp/frpc -c /root/frp/frpc.ini &

#nohup gunicorn -c /root/SBCv2/gunicorn.py SBC.wsgi -D &
#nohup  /usr/local/bin/python3 /root/SBCv2/manage.py runserver 0.0.0.0:92 --insecure  &
#nohup  python /root/SBCv2/manage.py runserver 0.0.0.0:92 --insecure  &


nohup gunicorn -c /root/SBCv2/gunicorn.py SBC.asgi:application  -k uvicorn.workers.UvicornWorker -D &

#gunicorn SBC.asgi:application  -k uvicorn.workers.UvicornWorker -b :8100 -w 2 --threads 3
#gunicorn app.wsgi:application --bind 0.0.0.0:8000 --reload & daphne -b 0.0.0.0 -p 8089 app.asgi:application &

