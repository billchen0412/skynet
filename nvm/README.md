# nvm

## Step 1. Download and install NVM

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

## Step 2. Add NVM to your shell configuration

add the command below into `~/.zshrc` or somewhere for initialization

```
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

## Step 3. Verify NVM is installed

```
nvm --version
```

## Step 4. Installing Node.js with NVM

```
nvm install --lts           # Install latest LTS version
nvm install 20.19.0         # Install specific version
nvm use 20.19.0             # Switch to version 20.19.0
nvm alias default 20.19.0   # Make it default on new shells
```
