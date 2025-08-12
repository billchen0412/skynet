# Reverse proxy


## Create docker network

Create a network so that the service inside docker share the same network.
```sh
docker network create skynet_network
```

## Bring up Nginx and Get Certificates

Start the proxy first:
```sh
cd reverse-proxy
docker compose up -d nginx
```

Request the initial cert (change email/domain):
```sh
docker compose run --rm certbot certonly --webroot \
  -w /var/www/certbot \
  -d cisc.tw \
  -d cloud.cisc.tw \
  --email billchen0412@gmail.com --agree-tos --non-interactive
```

Reload Nginx to load the new certs:
```sh
docker compose exec nginx nginx -s reload
```


<!-- ## Step 1: Install Nginx

```sh
sudo apt update
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

curl http://localhost
```

## Step 2: (Optional) Allow Nginx in the firewall

```
sudo ufw allow 'Nginx Full'
sudo ufw reload
```

## Step 3: Create an Nginx site config for your Nextcloud domain

`sudo vi /etc/nginx/sites-available/nextcloud`

```
server {
    listen 80;
    server_name nextcloud.hkchen.cc;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Step 4: Enable the config and reload Nginx

```sh
sudo ln -s /etc/nginx/sites-available/nextcloud /etc/nginx/sites-enabled/
sudo nginx -t    # test config syntax
sudo systemctl reload nginx
```

## Step 5: Change Nextcloud to listen on port 8080 (if using Docker)

```yml
services:
  app:
    image: nextcloud
    ports:
      - "8080:80"     # maps host:container
    ...
```

## Step 6: Add DNS record

Set up a DNS A record:
- nextcloud.hkchen.cc → your server’s public IP

## Optional Step 7: Add HTTPS (SSL)

```
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d nextcloud.hkchen.cc
``` -->
