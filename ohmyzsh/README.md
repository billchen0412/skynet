# oh-my-zsh and zplug

## oh-my-zsh

### install

`sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"`

### setup

`mkdir ~/.zsh`

`touch ~/zsh/10_env.sh`

`vi ~/.zshrc` and paste command below

```sh
source ~/.zsh/10_env.zsh
```

## zplug

### install

`curl -sL --proto-redir -all,https https://raw.githubusercontent.com/zplug/installer/master/installer.zsh | zsh`

### setup

`vi ~/.zsh/zplug.zsh`
```sh
zplug 'zplug/zplug', hook-build:'zplug --self-manage'

# libs
zplug "lib/completion", from:oh-my-zsh, defer:0
zplug "lib/directories", from:oh-my-zsh, defer:0
zplug "lib/grep", from:oh-my-zsh, defer:0
zplug "lib/key-bindings", from:oh-my-zsh, defer:0
zplug "lib/history", from:oh-my-zsh, defer:0
zplug "lib/misc", from:oh-my-zsh, defer:0

# Add zplug plugins
zplug "~/.zsh", from:local, use:"<->_*.zsh"
zplug "plugins/git",   from:oh-my-zsh
zplug "plugins/colored-man-pages", from:oh-my-zsh
zplug "plugins/kubectl", from:oh-my-zsh
zplug "plugins/docker", from:oh-my-zsh
zplug "plugins/docker-compose", from:oh-my-zsh

zplug "romkatv/powerlevel10k", as:theme, depth:1
zplug "zsh-users/zsh-syntax-highlighting", defer:2
zplug "zsh-users/zsh-history-substring-search", as:plugin
zplug "zsh-users/zsh-autosuggestions", defer:3
```

```
zplug 'zplug/zplug', hook-build:'zplug --self-manage'

# libs
zplug "lib/completion", from:oh-my-zsh, defer:0
zplug "lib/directories", from:oh-my-zsh, defer:0
zplug "lib/grep", from:oh-my-zsh, defer:0
zplug "lib/key-bindings", from:oh-my-zsh, defer:0
zplug "lib/history", from:oh-my-zsh, defer:0
zplug "lib/misc", from:oh-my-zsh, defer:0
#zplug "lib/termsupport", from:oh-my-zsh, defer:0

# Add zplug plugins
zplug "~/.zsh", from:local, use:"<->_*.zsh"
zplug "plugins/git",   from:oh-my-zsh
zplug "plugins/colored-man-pages", from:oh-my-zsh
zplug "plugins/kubectl", from:oh-my-zsh
zplug "plugins/docker", from:oh-my-zsh
zplug "plugins/docker-compose", from:oh-my-zsh
#zplug "plugins/aws", from:oh-my-zsh
zplug "rupa/z", use:"z.sh"
#zplug "mafredri/zsh-async"
#zplug "sindresorhus/pure", use:"pure.zsh", as:theme
zplug "fcambus/ansiweather"
zplug "ael-code/zsh-colored-man-pages"
zplug "fabiokiatkowski/exercism.plugin.zsh"
#zplug "junegunn/fzf-bin", as:command, from:gh-r, rename-to:"fzf", frozen:1
#zplug "starship/starship", as:command, from:gh-r, rename-to:"starship"
#zplug "stedolan/jq", from:gh-r, as:command, rename-to:"jq"
#zplug "mikefarah/yq", from:gh-r, as:command, rename-to:"yq"
#zplug "sharkdp/bat", from:gh-r, as:command, rename-to:"bat"
#zplug "dandavison/delta", from:gh-r, as:command, rename-to:"delta"
#zplug "Peltoche/lsd", from:gh-r, as:command, rename-to:"lsd"
#zplug "BurntSushi/ripgrep", from:gh-r, as:command, rename-to:"rg"
#zplug "sharkdp/fd", from:gh-r, as:command, rename-to:"fd"

zplug "zdharma/fast-syntax-highlighting", defer:3
zplug "zsh-users/zsh-history-substring-search", defer:3
zplug "zsh-users/zsh-autosuggestions", defer:3
```


add the command below into `~/.zshrc` or somewhere for initialization

```sh
if [[ -f ~/.zplug/init.zsh ]]; then
    export ZPLUG_LOADFILE=~/.zsh/zplug.zsh
    source ~/.zplug/init.zsh

    if ! zplug check --verbose; then
        printf "Install? [y/N]: "
        if read -q; then
            echo; zplug install
        fi
        echo
    fi
    zplug load
fi
```