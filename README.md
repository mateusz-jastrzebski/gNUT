# gNUT (graphical Network UPS Tools)

Graphical webservice for centralized NUT's upsd server.

Inspired by [Rshipp's webNUT](https://github.com/rshipp/webNUT) but rewritten in Django.

Authentication is possible with randomly generated Django superuser password and LDAP.

Currently program supports changing UPS driver's parameters, that are essential for a proper client emergency shutdown. No more fiddling with editing the file manually on the production server!


## [Click here for Installation setup](#installation)

## Development

#### If you want to contribute to this project, uncomment `Debug=True` inside `.env` file and edit it with your needs


## It is best suited to test this webservice with a UPS running somewhere nearby

>If you don't have an opportunity to have one, you can use the `dummy-ups` driver
>
>The `ups.conf` file that is inside the repo is currently configured to use such a driver
>
>You can modify and/or add dummy drivers however you like, they can even share the same or multiple sequence files
>```
>[test]
>driver = dummy-ups
>port = test.seq
>desc = "Test driver"
>```
>Then edit the sequence file `test.seq` with your desired UPS outputs loop
>
>You can use any UPS variables here that are possible to access using `upsc` command.
>
>The following sequence will switch `ups.status` from On-Line to On-Battery each 15 seconds.
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

4. Run migrate

```
python3 manage.py migrate
```

5. Create superuser

```
python3 manage.py createdefaultadmin
```

6. The credentials are written to the `superuser.txt` file

```
sudo docker exec -it gnut sh -c 'cat superuser.txt'
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

1. Make a directory for your files and download files needed for starting the application

```
mkdir -p gnut/ups_config gnut/db_data
wget -O gnut/docker-compose.yml https://raw.githubusercontent.com/mateusz-jastrzebski/gNUT/master/docker-compose.yml
wget -O gnut/.env https://raw.githubusercontent.com/mateusz-jastrzebski/gNUT/master/.env
```

**For servers using the obsolete `docker-compose` package (instead of `docker compose` plugin) uncomment the `version` line in `docker-compose.yml`**

2. Insert your configs

*At this moment gNUT **does not** let you create configs from the web app (just edit existing ones), keep in touch..*

Fill in data in `.env` (for gNUT configuration) and `docker-compose.yml` when using containers bundle (mjast/nutgalaxy5500 or other NUT version + reverse proxy)


`gnut/ups_config/upsd.users`

```
[<ADMIN_NAME>]
password=<ADMIN_PASSWORD>
actions=SET
upsmon master
[<SLAVE_NAME>]
password=<SLAVE_PASSWORD>
upsmon slave
```

`gnut/ups_config/ups.conf`

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

`gnut/ups_config/upsmon.conf`

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

3. Generate a secret key and paste it into `.env` file

```
tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' </dev/urandom | head -c 32;
```

`gnut/.env`

```
SECRET_KEY=<COPIED_SECRET_KEY>
```

4. Setup a service for rootless `ups-monitor` restart (if host needs to be shutdown)

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

5. Run `docker-compose up -d`

6. Default superuser credentials:

```
sudo docker exec -it gnut sh -c 'cat superuser.txt'
```

7. For testing you can either type:

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
