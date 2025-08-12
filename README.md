

# Btrfs

## 快照

```
# sudo apt-get install -y btrbk
# sudo vim /etc/btrbk/btrbk.conf
transaction_log /var/log/btrbk.log
timestamp_format long
snapshot_dir .snapshots
snapshot_preserve 14d

volume /mnt/btrfs-root
  subvolume @home
    snapshot_create always
    snapshot_preserve_min 7d
    snapshot_preserve 14d
  subvolume @docker
    snapshot_create always
    snapshot_preserve_min 3d
    snapshot_preserve 7d
```

## 自動每天執行

```
# sudo vim /etc/systemd/system/btrbk-daily.service
[Unit]
Description=Daily Btrbk Snapshot

[Service]
ExecStart=/usr/bin/btrbk run
```

```
# sudo vim /etc/systemd/system/btrbk-daily.timer
[Unit]
Description=Run Btrbk Daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```
sudo mkdir /mnt/btrfs-root/.snapshots
sudo chmod 700 /mnt/btrfs-root/.snapshots

sudo systemctl daemon-reexec
sudo systemctl enable --now btrbk-daily.timer
sudo btrbk run
sudo btrfs quota enable /mnt/btrfs-root
sudo btrfs quota rescan -w /mnt/btrfs-root
sudo btrfs qgroup show -pcre /mnt/btrfs-root
```

### check disk quota tool

```
sudo btrfs quota enable /mnt/btrfs-root
sudo btrfs quota rescan -w /mnt/btrfs-root
sudo btrfs qgroup show -pcre /mnt/btrfs-root
```

### Regular check disk report

```
tutul@mail(05:23:31):/home/tutul
>> cat /home/tutul/btrfs/regular-email.sh 
#!/bin/bash

MOUNT_POINT="/mnt/btrfs-root"
EMAIL="moss12333@gmail.com"
LOG_FILE="/var/log/btrfs_health.log"

# 執行 scrub
btrfs_scrub() {
    btrfs scrub start -B $MOUNT_POINT
    local status=$?
    echo "Scrub completed with status: $status" >> $LOG_FILE
    return $status
}

# 檢查 RAID 狀態
check_raid() {
    local raid_status=$(btrfs device stats $MOUNT_POINT)
    echo "RAID Status: $raid_status" >> $LOG_FILE
    return $(echo "$raid_status" | grep -c "error")
}

# 檢查空間使用
check_space() {
    local space_info=$(btrfs filesystem usage $MOUNT_POINT)
    echo "Space Usage: $space_info" >> $LOG_FILE
    echo "$space_info"
}

# 生成報告
generate_report() {
    {
        echo "BTRFS Health Report - $(date)"
        echo "=========================="
        echo
        check_space
        echo
        btrfs device stats $MOUNT_POINT
        echo
        btrfs filesystem show
    } | mail -s "BTRFS Weekly Report" $EMAIL
}
btrfs_scrub
check_raid
generate_report
```

### ssh

```
# 建立 ssh key
mkdir -p /home/tutul/.ssh
chown -R tutul:tutul /home/tutul/.ssh
chmod 700 /home/tutul/.ssh
chown -R tutul:tutul /home/tutul/.ssh
# 回到mac local 本機
ssh-keygen 

vim /etc/ssh/sshd_config
# 請先建立好key並在另個console測試好
---
PermitRootLogin no
PasswordAuthentication no
---
systemctl restart sshd
```


### Oh my zsh

```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# 可以依照習慣編輯 zshrc
# vim .zshrc
```