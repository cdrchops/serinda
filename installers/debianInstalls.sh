#!/bin/bash
#https://www.windowscentral.com/how-backup-windows-subsystem-linux-wsl-distribution
sudo apt update && sudo apt upgrade
#sudo apt dist-upgrade
sudo apt-get install git wget curl zip unzip lsb-release gnupg sshpass python3 python3-pip
sudo apt-get install python3-pip cmake wget lsb-release curl zip mariadb-client mariadb-server

curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
#sdk install java 8.0.292.j9-adpt - was renamed temurin the below install is the equivalent
sdk install java 8.0.352-tem

# sdk install gradle 6.9.2
# for grooscript
sdk install gradle 3.5
sdk install grails 4.0.11

#https://serverspace.io/support/help/how-to-install-mysql-on-debian-10/
#sudo apt-get install default-mysql-server #don't use this one
wget https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.22-1_all.deb
#apt-get update
#sudo apt install mysql-server
#sudo apt-get install mysql-community-server
#/usr/bin/mysql -u root -p

curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash 
source ~/.bashrc

export NVM_DIR="$HOME/.nvm"
source ~/.bashrc

nvm install node
# npm install gulp-cli


# rust install for use with snips
# windows may require a different installer
# https://www.rust-lang.org/tools/install
# add %USERPROFILE%\.cargo\bin to windows environment variables
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"

#/home/winkdoubleguns/.cargo/bin
#/home/winkdoubleguns/.profile
#/home/winkdoubleguns/.bashrc
