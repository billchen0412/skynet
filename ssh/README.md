# ssh

## install

```sh
sudo apt update
sudo apt install -y openssh-server
```

## start up service

```sh
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
```

## set up .ssh folder

```
# 建立 ssh key
mkdir -p /home/hkchen/.ssh
chown -R hkchen:hkchen /home/hkchen/.ssh
chmod 700 /home/hkchen/.ssh
chown -R hkchen:hkchen /home/hkchen/.ssh
```

## generate key at local

```sh
ssh-keygen
# suggest using ed25519 and phrase for accessing public key
```

## connect to server

```sh
ssh server_ip -l hkchen
```

## remove some config

請確認前一步驟的連線有成功在做這一步驟

PermitRootLogin -> 不允許 root 登入

PasswordAuthentication -> 不允許密碼登入 (只能透過 public key)

`vim /etc/ssh/sshd_config`
```
PermitRootLogin no
PasswordAuthentication no
```

`systemctl restart sshd`
