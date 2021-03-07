## Update repository
apt update -qq
apt full-upgrade -qq -y

## install all necessary apt packages
# python3 to run camera-timer program
# redis to store camera times
# git to clone software from github
apt install python3 redis git


## install python packages for camera-timer
# RPi.GPIO to control RPi GPIOs
# redis to communicate with internal redis db
# flask to run the webserver for the settings
pip3 install RPI.GPIO redis flask