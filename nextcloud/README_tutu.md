# nextcloud

## install 
### docker-compose.yml
```yml
volumes:
  nextcloud:
  db:

services:
  redis:
    image: redis:alpine
    restart: always

  db:
    image: mariadb:10.6
    restart: always
    command: --transaction-isolation=READ-COMMITTED --log-bin=binlog --binlog-format=ROW
    volumes:
      - db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=
      - MYSQL_PASSWORD=
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  app:
    image: nextcloud:30.0.2
    pull_policy: always
    restart: always
    command: |
      bash -c '
      /manual_scripts/init.sh &&
      apache2-foreground'
    extra_hosts:
      - "mail.tutul.today:172.19.0.1"
    ports:
      - 80:80
      - 443:443
    depends_on:
      - redis
      - db
    volumes:
      - nextcloud:/var/www/html
      - /mnt/skydata/NextCloud/data:/var/www/html/data
      - /mnt/skydata/NextCloud/config:/var/www/html/config
      - /mnt/skydata/NextCloud/custom_apps:/var/www/html/custom_apps
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
      - ./apache/conf:/etc/apache2/sites-available
      - ./manual_scripts:/manual_scripts
    environment:
      - MYSQL_PASSWORD=
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_HOST=db
      - NEXTCLOUD_ADMIN_USER=
      - NEXTCLOUD_ADMIN_PASSWORD=
      - PHP_UPLOAD_LIMIT=10G
      - PHP_MEMORY_LIMIT=2G
      - NEXTCLOUD_TRUSTED_DOMAINS=192.168.68.202
  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    command: certonly -v --webroot -w /var/www/certbot --force-renewal --email moss12333@gmail.com -d tutul.today -d mail.tutul.today --agree-tos --no-eff-email
		depends_on:
      - app
```
### apache conf
```sh
mkdir -p apache/conf
# fist conf 
# 一定要先用這個，主要是先產生 ssl憑證必須要cerbot
vim apache/conf/000-default.conf
<VirtualHost *:80>
    ServerName tutul.today
	  ServerAlias mail.tutul.today
    
    Alias /.well-known/acme-challenge/ /var/www/certbot/.well-known/acme-challenge/
    <Directory "/var/www/certbot/">
        AllowOverride None
        Options None
        Require all granted
    </Directory>
	  LimitRequestBody 0
</VirtualHost>
# 有了憑證就可以更換成 ssl的conf
vim apache/conf/default-ssl.conf
<VirtualHost *:80>
    ServerName tutul.today
    ServerAlias mail.tutul.today
    
    Alias /.well-known/acme-challenge/ /var/www/certbot/.well-known/acme-challenge/
    <Directory "/var/www/certbot/">
        AllowOverride None
        Options None
        Require all granted
    </Directory>

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/.well-known/acme-challenge/ [NC]
    # 檢查是否是 mail 子域名
    RewriteCond %{HTTP_HOST} !^mail\. [NC]
    RewriteCond %{HTTPS} off
    RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
    
    RewriteCond %{HTTP_HOST} ^mail\. [NC]
    RewriteCond %{REQUEST_URI} !^/.well-known/acme-challenge/ [NC]
    RewriteRule ^ - [F]

    LimitRequestBody 0
</VirtualHost>
<VirtualHost *:443>
    ServerName tutul.today
    ServerAdmin moss12333@gmail.com
    DocumentRoot /var/www/html
    
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/tutul.today/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/tutul.today/privkey.pem

    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    LimitRequestBody 0
</VirtualHost>
```
### manual_scripts (need sudo) in machine
```sh
mkdir -p manual_scripts
vim manual_scripts/init.sh
#!/usr/bin/sh
apt update
apt install -y vim less cron
apt -y install libsmbclient-dev libmagickwand-dev && pecl install smbclient
echo 'extension=smbclient.so' > /usr/local/etc/php/conf.d/docker-php-ext-smbclient.ini
a2enmod rewrite ssl
a2enmod headers

if ! grep -q "2 => 'tutul.today'" /var/www/html/config/config.php; then
    sed -i "/1 => '192\.168\.68\.202',/a\    2 => 'tutul.today'," /var/www/html/config/config.php
else
    echo "Entry '2 => tutul.today' already exists. No changes made."
fi

a2ensite default-ssl.conf
a2dissite 000-default.conf

bash -c 'echo "*/5 * * * * export PHP_MEMORY_LIMIT=2G; /usr/local/bin/php -f /var/www/html/cron.php --define apc.enable_cli=1 >> /var/www/cron.log 2>&1" > /tmp/www-data-crontab && crontab -u www-data /tmp/www-data-crontab && rm /tmp/www-data-crontab'
service cron start
```
### docker first time install
```sh 
docker compose up -d
docker-compose exec app /manual_scripts/init.sh
docker-compose exec --user www-data app php occ app:enable files_external
docker-compose exec --user www-data app php occ config:system:set maintenance_window_start --type=integer --value=16
docker-compose exec --user www-data app php occ config:system:set default_phone_region --type=string --value=TW
docker-compose exec --user www-data app php occ config:system:set redis host --type=string --value='redis'
docker-compose exec --user www-data app php occ config:system:set redis port --type=integer --value=6379
docker-compose exec --user www-data app php occ config:system:set redis timeout --type=float --value=0.0
docker-compose exec --user www-data app php occ config:system:set memcache.locking --type=string --value='\OC\Memcache\Redis'
docker-compose exec app bash -c 'echo "*/5 * * * * export PHP_MEMORY_LIMIT=2G; /usr/local/bin/php -f /var/www/html/cron.php --define apc.enable_cli=1 >> /tmp/cron.log 2>&1" > /tmp/www-data-crontab && crontab -u www-data /tmp/www-data-crontab && rm /tmp/www-data-crontab'
docker-compose exec --user www-data app php occ app:install passwords
```

## update or recreate instance nextcloud version
```sh
docker-compose exec --user www-data app php occ maintenance:mode --on
docker compose down
# vim docker-compose.yml and change image version
docker compose up -d
docker-compose exec --user www-data app php occ maintenance:mode --off
```

## renew ssl certification
```sh
vim renew-ssl.sh
#!/bin/bash
set -e
set -x
cd /home/tutul/nextcloud
docker-compose run --rm certbot
docker-compose exec app apache2ctl graceful
```
## set renew crontab
```sh
crontab -e
0 0 1 * * /home/tutul/nextcloud/renew-ssl.sh >> /home/tutul/nextcloud/ssl_renewal.log 2>&1
```


## see backgroud task
```
docker-compose exec --user www-data app php occ background-job:list
```

## add files manully 
```
docker-compose exec --user www-data app php occ files:scan --path /luke/files
```