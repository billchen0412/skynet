# VPN (WireGuard)

`sudo apt-get install -y wireguard-tools`

`sudo vim /etc/wireguard/wg0.conf`
```
要到wireguard下載連線檔案，然後直接複製貼上即可
```

# sudo wg-quick down wg0

`sudo systemctl enable wg-quick@wg0.service`

`sudo systemctl start wg-quick@wg0.service`

`sudo systemctl status wg-quick@wg0.service  # check service is active`

# 避免重新開機時與其他服務衝突

`sudo systemctl edit wg-quick@.service`

```
[Unit]
# 等網路完全啟動
After=network-online.target nss-lookup.target docker.service firewalld.service containerd.service
Wants=network-online.target nss-lookup.target
```

# execute command below to start up

`sudo systemctl daemon-reexec`

`sudo systemctl daemon-reload`

`sudo systemctl restart wg-quick@wg0.service`