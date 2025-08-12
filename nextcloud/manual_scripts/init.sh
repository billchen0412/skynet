#!/usr/bin/sh
apt update
apt install -y vim less cron

# create a cronjob to trigger cron.php every 5 minutes
bash -c 'echo "*/5 * * * * export PHP_MEMORY_LIMIT=2G; /usr/local/bin/php -f /var/www/html/cron.php --define apc.enable_cli=1 >> /tmp/cron.log 2>&1" > /tmp/www-data-crontab && crontab -u www-data /tmp/www-data-crontab && rm /tmp/www-data-crontab'
service cron start
