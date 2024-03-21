#!/bin/bash
mount -t ntfs-3g /dev/sda1 /mnt/SBC
nohup gunicorn -c /root/SBCv2/gunicorn.py SBC.wsgi  -D &
nginx
nohup /root/frp/frpc -c /root/frp/frpc.ini &

#nohup gunicorn -c /root/SBCv2/gunicorn.py SBC.wsgi -D &
nohup  /usr/local/bin/python3 /root/SBCv2/manage.py runserver 0.0.0.0:92 --insecure  &

