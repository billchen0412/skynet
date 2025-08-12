# nextcloud

## create btrfs subvolume

```sh
sudo btrfs subvolume list /mnt/btrfs-root
sudo btrfs subvolume create /mnt/btrfs-root/@nextcloud

sudo mkdir -p /mnt/btrfs-root/@nextcloud/data
sudo chown -R 33:33 /mnt/btrfs-root/@nextcloud/data

sudo mkdir -p /mnt/btrfs-root/@nextcloud/config
sudo chown -R 33:33 /mnt/btrfs-root/@nextcloud/config

sudo mkdir -p /mnt/btrfs-root/@nextcloud/custom_apps
sudo chown -R 33:33 /mnt/btrfs-root/@nextcloud/custom_apps
```

## install nextcloud

### Create docker network

Create a network so that the service inside docker share the same network.
```
docker network create nextcloud_network
```

### make init script executable

```sh
chmod +x manual_scripts/init.sh
```

### start docker container
```sh
sudo apt-get install docker-compose-v2
docker compose up -d
```

### docker first time install
```sh 
docker compose up -d
docker compose exec app /manual_scripts/init.sh
docker compose exec --user www-data app php occ app:enable files_external
docker compose exec --user www-data app php occ config:system:set maintenance_window_start --type=integer --value=16
docker compose exec --user www-data app php occ config:system:set default_phone_region --type=string --value=TW
docker compose exec --user www-data app php occ config:system:set redis host --type=string --value='nextcloud_redis'
docker compose exec --user www-data app php occ config:system:set redis port --type=integer --value=6379
docker compose exec --user www-data app php occ config:system:set redis timeout --type=float --value=0.0
docker compose exec --user www-data app php occ config:system:set memcache.locking --type=string --value='\OC\Memcache\Redis'
docker compose exec --user www-data app php occ app:install passwords
```

## update or recreate instance nextcloud version

```sh
docker compose down
# vim docker-compose.yml and change image version
docker compose up -d
```


## see backgroud task
```
docker-compose exec --user www-data app php occ background-job:list
```

## add files manully 
```
docker-compose exec --user www-data app php occ files:scan --path /luke/files
```