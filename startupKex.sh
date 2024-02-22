sudo umount /tmp/.X11-unix
#sudo rm -rf /tmp/.X* (if '/tmp/.X11-unix' exists)
sudo rm -rf /tmp/.X*
sudo mkdir /tmp/.X11-unix
sudo chmod 1777 /tmp/.X11-unix
sudo chown root /tmp/.X11-unix/
sudo tigervncserver -xstartup /usr/bin/xterm
export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0.0
sudo kex start
sudo kex --win -s
