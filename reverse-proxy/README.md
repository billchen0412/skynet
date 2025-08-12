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
# Issue cert for each domain
docker compose run --rm certbot certonly --webroot \
  -w /var/www/certbot \
  -d cisc.tw \
  --email billchen0412@gmail.com --agree-tos --non-interactive
docker compose run --rm certbot certonly --webroot \
  -w /var/www/certbot \
  -d cloud.cisc.tw \
  --email billchen0412@gmail.com --agree-tos --non-interactive
```

Reload Nginx to load the new certs:
```sh
docker compose exec nginx nginx -s reload
```
