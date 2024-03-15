#mount -t ntfs-3g /dev/sda1 /mnt/soft
#mount -t ntfs-3g /dev/sdc /mnt/SBC
nohup sh /root/MountDisk.sh &
#sh /mnt/soft/SBCv2/gunicorn.sh
cd /root/SBCv2 && nohup gunicorn -c gunicorn.py SBC.wsgi  -D &
nginx
nohup /root/frp/frpc -c /root/frp/frpc.ini &
nohup  python3 /root/SBCv2/manage.py runserver 0.0.0.0:92 --insecure  &

