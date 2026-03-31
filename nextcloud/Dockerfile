FROM nextcloud:32.0.6-apache

# 安裝工具
RUN apt-get update && apt-get install -y \
    vim \
    less \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 寫入 Cron 設定 (注意這裡要指定執行使用者為 www-data)
RUN echo "*/5 * * * * www-data php -f /var/www/html/cron.php --define apc.enable_cli=1 >> /tmp/cron.log 2>&1" > /etc/cron.d/nextcloud-cron \
    && chmod 0644 /etc/cron.d/nextcloud-cron

# 建立 Hook 腳本啟動服務
RUN mkdir -p /docker-entrypoint-init.d && \
    echo "#!/bin/sh\nservice cron start" > /docker-entrypoint-init.d/start-cron.sh && \
    chmod +x /docker-entrypoint-init.d/start-cron.sh