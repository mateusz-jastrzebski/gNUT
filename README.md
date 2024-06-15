# gNUT

Acts as a graphical interface website for centralized NUT's upsd server.
Inspired by [Rshipp's webNUT](https://github.com/rshipp/webNUT) but rewritten in Django

Authentication is possible with LDAP or with 

## [Click here for Installation setup](#installation)

## Development

#### If you want to develop this project, firstly create a `.env` file with environmental variables needed for startup

`.env`

```
DEBUG=True

SECRET_KEY=<YOUR_KEY>

# This does not really matter for testing
#CSRF_TRUSTED_ORIGINS=<YOUR_DOMAIN>

TZ=<YOUR_TZ>

# If you want LDAP based auth
#LDAP_SERVER=<YOUR_LDAP_SERVER_IP>:<PORT>
#LDAP_AUTH_SEARCH_BASE=ou=People,dc=<YOUR_DOMAIN>,dc=<YOUR_DOMAIN>,dc=<YOUR_DOMAIN>
# Optional, all users existing in LDAP can see admin page if not set
#REQUIRED_GROUP=cn=<YOUR_GROUP>,ou=Groups,dc=<YOUR_DOMAIN>,dc=<YOUR_DOMAIN>,dc=<YOUR_DOMAIN>
```

## Then obviously you should have a UPS running somewhere

>If you don't you can use `dummy-ups` driver
>
>In `ups.conf` type:
>```
>[test]
>driver = dummy-ups
>port = test.seq
>desc = "Test driver"
>```
>Then create a file `test.seq` in the same folder with your desired UPS outputs loop
>```
>battery.charge: 100
>ups.load: 15
>battery.charge.low: 10
>ups.status: OL
>TIMER 15
>ups.status: OB
>TIMER 15
>```
>NOTE: for this time being you **NEED** to provide `battery.charge`, `ups.load` and `battery.charge.low`
>otherwise the server won't start

1. Create virtual environment

```
python3 -m venv venv
```

2. Activate virtual environment

_On Linux / MacOS_

```
source venv/bin/activate
```

_On Windows_

```
.\\venv\Scripts\activate.bat
```

3. Install requirements

```
pip3 install -r requirements.txt
```

4. Create superuser

```
python3 manage.py createsuperuser
```

5. Run server

```
python3 manage.py runserver 0.0.0.0:8000
```

or

```
gunicorn --bind 0.0.0.0:8000 webNUT.wsgi:application
```

## Installation

>At this moment this app is only suited for Docker deploy + apt installable `systemd` based `nut-monitor`- available in `nut-client` package.

## For Clients config please read [this](CLIENTS.md) readme.

## Docker deploy

1. Make a directory for your files

2. Create a directory inside it for your NUT configs

*At this moment gNUT **does not** let you create configs from the web app (just edit existing ones), keep in touch..*

3. Insert your configs


`upsd.users`

```
[<ADMIN_NAME>]
password=<ADMIN_PASSWORD>
actions=SET
upsmon master
[<SLAVE_NAME>]
password=<SLAVE_PASSWORD>
upsmon slave
```

`ups.conf`

```
maxretry = 5

[<UPS_NAME>]
driver = snmp-ups
mibs = apcG5500
port = <UPS_IP>
community = public
snmp_version = v1
pollfreq = 15
desc = "UPS for shutting down non critical servers"
ignorelb
override.battery.charge.low = 50
[<UPS_NAME>]
driver = snmp-ups
mibs = apcG5500
port = <UPS_IP>
community = public
snmp_version = v1
pollfreq = 15
desc = "UPS for shutting down critical servers"
ignorelb
override.battery.charge.low = 30
[<UPS_NAME>]
driver = snmp-ups
mibs = apcG5500
port = <UPS_IP>
community = public
snmp_version = v1
pollfreq = 15
desc = "UPS for shutting ONLY this server"
ignorelb
override.battery.charge.low = 15
```

`upsmon.conf`

```
MINSUPPLIES <NUMBER_OF_UPS_NEEDED_FOR_STAYING_UP>
SHUTDOWNCMD "/sbin/shutdown -h +0"
POLLFREQ 5
POLLFREQALERT 5
HOSTSYNC 15
DEADTIME 15
POWERDOWNFLAG /etc/killpower
RBWARNTIME 43200
NOCOMMWARNTIME 300
FINALDELAY 5
MONITOR <UPS_NAME>@localhost 1 <ADMIN_NAME> <ADMIN_PASSWORD> master
<REPEAT_FOR_EACH_UPS_YOU_WANT_THIS_SYSTEM_TO_RELY_ON>
```

4. Create a .env file in the top directory

5. Generate a secret key and paste it into `.env` file

```
tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' </dev/urandom | head -c 32;
```

`.env`

```
SECRET_KEY=<COPIED_SECRET_KEY>
```

6. Setup a service for rootless `ups-monitor` restart (if host needs to be shutdown)

`/usr/lib/systemd/system/upsmon-file-restart.service`

```
[Unit]
Description=File Monitor Service

[Service]
Type=oneshot
ExecStart=/bin/systemctl restart nut-monitor
Restart=no
RestartSec=0

[Install]
WantedBy=multi-user.target
```

`/usr/lib/systemd/system/upsmon-file-restart.path`

```
[Unit]
Description=File Monitor Path Unit

[Path]
PathChanged=<ABSOLUTE_PATH_TO_YOUR_do-not-touch_FILE>

[Install]
WantedBy=multi-user.target
```

Then edit `/etc/nut/nut.conf`

```
MODE=netclient
```

Delete `/etc/nut/upsmon.conf` and set a symbolic link from your `ups_config` folder

7. Run `docker-compose up -d`

8. If configured not to work with LDAP, create superuser with this command

```
docker exec -it gnut python3 manage.py createsuperuser
```

9. For testing you can either type:

```
upsc -l
```

or after a few seconds of starting the gNUT app the UPSes should be visible on the page

## Systemd deploy (WIP)

>This needs a bunch of care as I mainly moved to deploying this software with Docker

For systemd service deploy you also need to specify a couple of ENV variables for it to work

Ensure env variables are present for the app, then:

1. Install requirements

## to do, need to find linux packages to install eg. python3_xyz

2. Migrate 

```
python3 manage.py migrate
```

3. For a deploy you need a systemd service running

Create and edit `/etc/systemd/system/gunicorn.service`

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
# the specific user that our service will run as
User=<your_user>
Group=<your_group>
# another option for an even more restricted service is
# DynamicUser=yes
# see http://0pointer.net/blog/dynamic-users-with-systemd.html
RuntimeDirectory=gunicorn
WorkingDirectory=<your_absolute_directory>
ExecStart=/usr/bin/gunicorn webNUT.wsgi
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

5. Create and edit `/etc/systemd/system/gunicorn.socket`

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
# Our service won't need permissions for the socket, since it
# inherits the file descriptor by socket activation
# only the nginx daemon will need access to the socket
SocketUser=www-data
# Optionally restrict the socket permissions even more.
# SocketMode=600

[Install]
WantedBy=sockets.target
```

6. Enable gunicorn.socket

```
systemctl enable --now gunicorn.socket
```

7. Now go ahead and configure a chosen http server

Sample Nginx config (here configured for proxy over a port, not a socket)
```
server {
    listen 80;


    location /static/ {
        alias <your_absolute_directory>/static/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }


}
```

Sample Apache2 config (using UNIX socket)
```
<VirtualHost *:80>
    ServerName localhost

    DocumentRoot /home/student/Desktop/test-gNUT/gNUT-development

    <Proxy *>
        Order deny,allow
        Require all granted
    </Proxy>

    ProxyPass /static/ !
    ProxyPass / unix:/run/gunicorn.sock|http://localhost/

    Alias /static/ <your_absolue_directory>/static/

    <Directory <your_absolute_directory>>
        Order deny,allow
        Require all granted
        Options -Indexes
    </Directory>

</VirtualHost>
```

8. After you start your HTTP Server, the website should be all good and running

9. If you want to restart the Gunicorn use:

```
systemctl restart gunicorn.socket
```
