# Auto Shutdown

## create script file

sudo vim /usr/local/bin/shutdown-after-hours.sh
```
#!/bin/bash

# 設定下班時間（24小時制），這裡是晚上7點
OFF_HOUR=19

# 目前小時
HOUR=$(date +%H)
logger "[AutoShutdown] Start workday checking..."

# 如果小於下班時間就直接跳出
if [ "$HOUR" -lt "$OFF_HOUR" ]; then
  logger "[AutoShutdown] Still in working time"
  exit 0
fi

# 檢查是否有人透過 SSH 登入

#SSH_USERS=$(who | grep -c 'ssh')
SSH_USERS=$(who | awk '{print $NF}' | grep -cE '^\(.*\)$')

logger "[AutoShutdown] Check ssh connection"
# 若沒有人透過 SSH 登入，關機
if [ "$SSH_USERS" -eq 0 ]; then
  logger "[AutoShutdown] 下班後無 SSH 連線，自動關機"
  systemctl poweroff
fi
```

## setup service

sudo vim /etc/systemd/system/shutdown-after-hours.service
```
[Unit]
Description=Auto shutdown after hours if no SSH sessions

[Service]
Type=oneshot
ExecStart=/usr/local/bin/shutdown-after-hours.sh
```

sudo vim /etc/systemd/system/shutdown-after-hours.timer
```
[Unit]
Description=Hourly check for idle SSH after work hours

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

## set executable and check

sudo chmod +x /usr/local/bin/shutdown-after-hours.sh
sudo systemctl enable --now shutdown-after-hours.timer
sudo systemctl list-timers | grep shutdown

# Auto Shutdown at Weekend

## create script file

sudo vim /usr/local/bin/shutdown-on-weekend.sh
```
#!/bin/bash

DAY=$(date +%u)  # 1=Mon, ..., 7=Sun

logger "[AutoShutdown] Start weekend detecting..."
if [ "$DAY" -eq 6 ] || [ "$DAY" -eq 7 ]; then
  echo "今天是週末，自動關機"
  logger "[AutoShutdown] Weekend detected, shutting down."
  /usr/bin/systemctl poweroff
fi
```

## setup service

### check the last service when we boot the server

```
journalctl -b | grep 'Reached target'
>
Hint: You are currently not seeing messages from other users and the system.
      Users in groups 'adm', 'systemd-journal' can see all messages.
      Pass -q to turn off this notice.
 7月 24 18:04:46 skynet systemd[2059]: Reached target paths.target - Paths.
 7月 24 18:04:46 skynet systemd[2059]: Reached target timers.target - Timers.
 7月 24 18:04:46 skynet systemd[2059]: Reached target sockets.target - Sockets.
 7月 24 18:04:46 skynet systemd[2059]: Reached target basic.target - Basic System.
 7月 24 18:04:46 skynet systemd[2059]: Reached target default.target - Main User Target.
```

### create service file

sudo vim /etc/systemd/system/shutdown-on-weekend.service
```
[Unit]
Description=Shutdown on Saturday or Sunday
After=default.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/shutdown-on-weekend.sh

[Install]
WantedBy=default.target
```

## set executable and check

sudo chmod +x /usr/local/bin/shutdown-on-weekend.sh
sudo systemctl enable shutdown-on-weekend.service