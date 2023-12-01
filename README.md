```markdown
# VPN API Setup Guide

## Important:

For production:

- Set `Debug=False` in `vpn_app/settings.py`.
- Add your domain to `ALLOWED_HOSTS`.

Example:
```

python
ALLOWED_HOSTS=['domain.com']

```

## Setup Instructions

### 1. Install Required Packages:

```

bash
apt install -y python3 python3-pip python3-venv nginx python3-dev default-libmysqlclient-dev build-essential dos2unix sshpass

````

### 2. Setup Project:

```bash
# Copy files to the desired location
cp -r [your_project_directory] /opt/vpnapi

# Navigate to the project directory
cd /opt/vpnapi


# Install necessary python packages
pip3 install -r requirements.txt (pip install --break-system-packages -r requirements.txt)
pip3 install -r ansible_requirements.txt (pip install --break-system-packages -r ansible_requirements.txt)

# Install necessary Ansible roles
ansible-galaxy install -r api/ansible_helpers/requirements.yaml
ansible-galaxy install kyl191.openvpn
````

### 3. MySQL Configuration:

Edit the MySQL configuration at `vpn_app/mysql.cnf`.

### 4. Database Setup (Optional):

For a new database type other than MySQL:

1. Delete the migrations folder: `rm -r api/migrations`
2. Reapply migrations to seed schema:

```bash
python manage.py makemigrations api
python manage.py migrate
```

### 5. Swagger Configuration:

```bash
python3 manage.py setup # to generate static files for swagger
```

### 6. Publish Project:

```bash
python3 -m venv myprojectenv
source myprojectenv/bin/activate
pip install django gunicorn psycopg2-binary
pip install -r requirements.txt
python3 manage.py createsuperuser  # Create a superuser if none exist
python3 manage.py collectstatic --clear --noinput
ufw allow 8080
python3 manage.py runserver 0.0.0.0:8080  # Test if project is running
gunicorn --bind 0.0.0.0:8080 vpn_app.wsgi  # Test if gunicorn is working
deactivate
```

## System Configuration:

### Ansible:

Edit your Ansible configuration:

```bash
vi ~/.ansible.cfg

[defaults]
nocolor=True
```

### Gunicorn:

1. Configure the Gunicorn socket and service:

```bash
vi /etc/systemd/system/gunicorn.socket
vi /etc/systemd/system/gunicorn.service
```

2. Start and enable the Gunicorn socket:

```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

3. Check the Gunicorn socket:

```bash
file /run/gunicorn.sock # Output should be /run/gunicorn.sock: socket
sudo journalctl -u gunicorn.socket # In case of errors
```

4. Reload the Gunicorn service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo journalctl -u gunicorn # In case of errors
```

### Nginx:

1. Edit the Nginx site configuration:

```bash
vi /etc/nginx/sites-enabled/vpn
```

2. Test and restart Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Reference:

For more on Ansible installation and configuration, check [this DigitalOcean tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-20-04).

### 7. Configuration Files:

Update the following files:

- `settings.env`
- `openvpn_conf.json`

## OpenVPN Authentication:

```bash
cd api/ansible_helpers/Ansible/openvpn/roles/openvpn/files
dos2unix client-connect.sh
dos2unix client-disconnect.sh
dos2unix handleAuthorization.py
```

- On line 102, when the domain is `octovpn.net`, use HTTPS.
- Ensure the log file is created with `chmod 777`.
- Both `handleauthorization.py` and `conf.json` should have permissions set with `chmod 777`.

## Development Phase:

### Running the Project:

For testing:

1. If the database is empty, seed data using:

```bash
python3 manage.py setup
```

This will also create a superuser (`admin` with password `123.com.net`).

2. Run the project:

```bash
python3 manage.py runserver
```

- Visit the main page: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Access the admin dashboard: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

### Redis

```bash
apt install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
apt-get update
apt-get install redis
redis-server /etc/redis/redis.conf
vi /etc/redis/redis.conf
***  Change this ***
supervised systemd

sudo systemctl restart redis.service.service
sudo systemctl status redis-server.service
sudo systemctl enable redis-server.service

```

### Rabbitmq

```bash
vi rabbit.sh

#!/bin/sh

sudo apt-get install curl gnupg apt-transport-https -y

## Team RabbitMQ's main signing key
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
## Community mirror of Cloudsmith: modern Erlang repository
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg > /dev/null
## Community mirror of Cloudsmith: RabbitMQ repository
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.9F4587F226208342.gpg > /dev/null

## Add apt repositories maintained by Team RabbitMQ
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Provides modern Erlang/OTP releases
##
deb [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu jammy main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu jammy main

# another mirror for redundancy
deb [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu jammy main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-erlang/deb/ubuntu jammy main

## Provides RabbitMQ
##
deb [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu jammy main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu jammy main

# another mirror for redundancy
deb [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu jammy main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.novemberain.com/rabbitmq/rabbitmq-server/deb/ubuntu jammy main
EOF


## Update package indices
sudo apt-get update -y

## Install Erlang packages
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl

## Install rabbitmq-server and its dependencies
sudo apt-get install rabbitmq-server -y --fix-missing

```

```bash
chmod 777 rabbit.sh
./rabbit.sh
systemctl start rabbitmq-server
systemctl enable  rabbitmq-server
rabbitmqctl add_user admin dj5fmd95mdkSD
rabbitmqctl set_user_tags admin  administrator
```

### Celery Worker:

```bash
vi /var/www/celery.conf
CELERYD_NODES = "w1"
CELERY_BIN = "/var/www/vpnapi/myprojectenv/bin/celery"
CELERY_APP = "vpn_app"
```

```bash
vi /etc/systemd/system/celery.service
[UNIT]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=root
Group=root
#EnvironmentFile=/var/www/celery.conf
WorkingDirectory=/var/www/vpnapi
ExecStart=/var/www/vpnapi/myprojectenv/bin/celery -A vpn_app multi start W1 W2 W3 --loglevel=info --logfile="var/log/celery/%n%I.log" --pidfile="var/run/celery/%n.pid"
ExecStop=/var/www/vpnapi/myprojectenv/bin/celery -A vpn_app multi stopwait W1 W2 W3 --loglevel=info --logfile="var/log/celery/%n%I.log" --pidfile="var/run/celery/%n.pid"
ExecReload=/var/www/vpnapi/myprojectenv/bin/celery -A vpn_app multi restart W1 W2 W3 --loglevel=info --logfile="var/log/celery/%n%I.log" --pidfile="var/run/celery/%n.pid"

Restart=always
StartLimitInterval=10
StartLimitBurst=5

[Install]
WantedBy=multi-user.target
```

```bash
vi /etc/systemd/system/celerybeat.service
[UNIT]
Description=Celery Beat Service
After=network.target

[Service]
Type=simple
User=root
EnvironmentFile=/var/www/celery.conf
WorkingDirectory=/var/www/vpnapi
ExecStart=/bin/sh -c '${CELERY_BIN} -A vpn_app beat'

Restart=always

[Install]
WantedBy=multi-user.target
```

```bash

python3 manage.py migrate django_celery_results
python3 manage.py migrate django_celery_beat

systemctl daemon-reload
systemctl enable celery.service
systemctl start celery.service

systemctl enable celerybeat.service
systemctl start celerybeat.service
```

---

That's it! Your VPN API should now be set up and ready for use.

```

### Install Laravel

apt install composer
apt install php
sudo apt install php8.1-curl php8.1-dom php-fpm
composer install
composer update --no-scripts

php artisan serve --host=0.0.0.0 --port=8000

sudo systemctl start php8.1-fpm
sudo systemctl enable php8.1-fpm

sudo chown -R www-data:www-data /var/www/gui
sudo chmod -R 755 /var/www/gui
sudo chown -R www-data:www-data /var/www/gui/storage
sudo chmod -R 775 /var/www/gui/storage
sudo chown -R www-data:www-data /var/www/gui/bootstrap/cache
sudo chmod -R 775 /var/www/gui/bootstrap/cache
sudo chown -R www-data:www-data /var/www/gui/resources/views
sudo chmod -R 755 /var/www/gui/resources/views

You can use the above markdown to create a well-structured README for your GitHub repository.
```
