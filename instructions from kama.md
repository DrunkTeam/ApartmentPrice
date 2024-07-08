# Последовательности текущих действий для поднятия проекта на серваке Ubuntu
```bash
ssh kama@91.224.86.145
```

```bash
sudo -i
```

```bash
sudo apt update
sudo apt upgrade
```

```bash
sudo apt install python3.11
sudo apt install python3.11-venv
```

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
```

```bash
bash Anaconda3-2024.06-1-Linux-x86_64.sh
```
Anaconda3 will now be installed into this location:
/root/anaconda3
PREFIX=/root/anaconda3

installation finished.
Do you wish to update your shell profile to automatically initialize conda?
This will activate conda on startup and change the command prompt when activated.
If you'd prefer that conda's base environment not be activated on startup,
   run the following command when conda is activated:

conda config --set auto_activate_base false

You can undo this by running `conda init --reverse $SHELL`? [yes|no]

[no] >>> yes
no change     /root/anaconda3/condabin/conda
no change     /root/anaconda3/bin/conda
no change     /root/anaconda3/bin/conda-env
no change     /root/anaconda3/bin/activate
no change     /root/anaconda3/bin/deactivate
no change     /root/anaconda3/etc/profile.d/conda.sh
no change     /root/anaconda3/etc/fish/conf.d/conda.fish
no change     /root/anaconda3/shell/condabin/Conda.psm1
no change     /root/anaconda3/shell/condabin/conda-hook.ps1
no change     /root/anaconda3/lib/python3.12/site-packages/xontrib/conda.xsh
no change     /root/anaconda3/etc/profile.d/conda.csh
modified      /root/.bashrc

==> For changes to take effect, close and re-open your current shell. <==

Thank you for installing Anaconda3!

```bash
sudo apt-get install postgresql
```

```bash
sudo systemctl start postgresql
```

```bash
exit
```

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
sudo -i
```

```bash
conda create -n mlops python=3.11.0
```

```bash
conda activate mlops
```

```bash
pip install poetry==1.8.1
```

```bash
poetry install
```

```bash
exit
```

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

```bash
echo; echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"'
```

```bash
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

```bash
sudo apt-get install build-essential
```

```bash
mkdir ~/ApartmentPrice
```

```bash
cd ~/ApartmentPrice
```

```bash
git clone https://github.com/DrunkTeam/ApartmentPrice.git .
```

```bash
git checkout dev-kama
```

```bash
pip install poetry==1.8.1
```

```bash
poetry install
```

Current Python version (3.11.0) is not allowed by the project (3.10.13).
Please change python executable via the "env use" command.

Из-за этой ошибки надо поменять в файле poetry.lock поменять в последней строчке версию python с 3.10.13 на 3.11.0

```bash
git pull
```

