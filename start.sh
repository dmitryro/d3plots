kill -9 $(pidof uwsgi)
cd /var/www/vhosts/3dact.com/tdact
uwsgi -s /tmp/tdact.sock --manage-script-name -w tdact --daemonize=/var/www/vhosts/3dact.com/logs/uwsgi.log --emperor /etc/uwsgi/vassals --uid root --gid root  --master --processes 6 --threads 3
