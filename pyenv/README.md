# pyenv

## Step 1: Install dependencies

```
sudo apt update
sudo apt install -y \
  make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
  libffi-dev liblzma-dev git
```

## Step 2: Install pyenv

add the command below into `~/.zshrc` or somewhere for initialization

```
curl https://pyenv.run | bash
```

## Step 3: Add pyenv to your shell (e.g. bash, zsh)

vi ~/.zsh/10_env.sh
```
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Step 4: Verify installation

```
pyenv --version
```

## Step 5 (Optional): Install a Python version

```
pyenv install 3.10.6
pyenv global 3.10.6   # Set it as the default version
```