## Update repository
apt update -qq
apt full-upgrade -qq -y

## install all necessary apt packages
# python3 to run camera-timer program
# redis to store camera times
# git to clone software from github
apt install python3 redis git -y


## install python packages for camera-timer
# RPi.GPIO to control RPi GPIOs
# redis to communicate with internal redis db
# flask to run the webserver for the settings
pip3 install RPI.GPIO redis flask


## make directory for camera timer project
# /opt/camcontrol
mkdir /opt/camcontrol


## write cronjobs for camera timer jobs
# first job minutely to check if shot is due
# second job every day midnight to calculate new shot times
echo "* * * * * /usr/bin/python3 /opt/camcontrol/make_shot_if_due.py >/dev/null 2>&1" >> /etc/crontab
echo "2 0 * * * /usr/bin/python3 /opt/camcontrol/generate_shot_times.py" >> /etc/crontab

## write service file for web service
echo "[Unit]" >> /etc/systemd/system/camcontrol.service
echo "Description=Webinterface for camera control" >> /etc/systemd/system/camcontrol.service
echo "After=network.target" >> /etc/systemd/system/camcontrol.service
echo "" >> /etc/systemd/system/camcontrol.service
echo "[Service]" >> /etc/systemd/system/camcontrol.service
echo "User=root" >> /etc/systemd/system/camcontrol.service
echo "WorkingDirectory=/opt/camcontrol" >> /etc/systemd/system/camcontrol.service
echo "ExecStart=/usr/bin/python3 /opt/camcontrol/serve_web.py" >> /etc/systemd/system/camcontrol.service
echo "Restart=always" >> /etc/systemd/system/camcontrol.service
echo "" >> /etc/systemd/system/camcontrol.service
echo "[Install]" >> /etc/systemd/system/camcontrol.service
echo "WantedBy=multi-user.target" >> /etc/systemd/system/camcontrol.service

# start webservice
systemctl daemon-reload
systemctl enable camcontrol.service
systemctl restart camcontrol.service


## make filesystem as overlay
cd /home/pi
git clone https://github.com/JasperE84/root-ro.git
cd root-ro
chmod +x install.sh
sudo ./install.sh

reboot