sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password rootpass'
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password rootpass'
sudo apt-get update
sudo apt-get -y install mysql-server-5.5
sudo apt-get -y install python-pip
sudo apt-get install python-dev <<< Y
sudo apt-get install libmysqlclient-dev
sudo apt-get install python-scipy <<< Y
sudo apt-get install python-pandas <<< Y
cd /vagrant
sudo pip install -r bot/requirements-local.txt

sudo apt-get install zsh <<< Y
apt-get install git-core <<< Y
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh
sudo chsh -s /bin/zsh

if [ ! -f /var/log/databasesetup ];
then
    echo "CREATE DATABASE test_pm_new" | mysql -uroot -prootpass

    touch /var/log/databasesetup

    if [ -f /vagrant/data/initial.sql ];
    then
        mysql -uroot -prootpass wordpress < /vagrant/data/initial.sql
    fi
fi