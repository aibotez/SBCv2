#!/bin/bash
/usr/bin/gunicorn -c /root/SBCv2/gunicorn.py SBC.wsgi
#/usr/bin/gunicorn --workers 3 --bind 127.0.0.1:8080 SBC.wsgi:application
#/usr/local/python3/bin/python3 /root/SBCv2/manage.py runserver 0.0.0.0:90  --insecure