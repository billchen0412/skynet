# 使用你指定的版本作為基底
FROM nextcloud:31.0.14-apache

# 安裝必要的系統工具，並在安裝後清理快取以縮小 Image 體積
RUN apt-get update && apt-get install -y \
    vim \
    less \
    cron \
    && rm -rf /var/lib/apt/lists/*

# 設定 Cron 作業
# 這裡直接將 crontab 寫入系統目錄，並確保權限正確
RUN echo "*/5 * * * * www-data export PHP_MEMORY_LIMIT=2G; /usr/local/bin/php -f /var/www/html/cron.php --define apc.enable_cli=1 >> /tmp/cron.log 2>&1" > /etc/cron.d/nextcloud-cron \
    && chmod 0644 /etc/cron.d/nextcloud-cron

# 建立一個啟動腳本來取代你原本的 command 邏輯
# 這樣可以確保 cron 啟動後，原本的 apache2-foreground 也能正常執行
COPY <<EOF /entrypoint-custom.sh
#!/bin/bash
# 啟動 cron 服務
service cron start
# 執行原本 Nextcloud 的進入點
exec /entrypoint.sh apache2-foreground
EOF

RUN chmod +x /entrypoint-custom.sh

# 設定新的進入點
ENTRYPOINT ["/entrypoint-custom.sh"]