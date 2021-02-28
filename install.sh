if [ "$EUID" -ne 0 ]
  then echo "Script must be run as root"
  exit 1
fi

echo "Installing required dependencies"
apt-get install python3-pip
pip3 install adafruit-circuitpython-ssd1306
apt-get install python3-pil
apt-get install -y python-smbus
apt-get install -y i2c-tools
pip3 install psutil

echo "Enabling I2C and SPI"
raspi-config nonint do_i2c 0
raspi-config nonint do_spi 0

echo "Linking service"
sudo ln -s $PWD/screen.service /lib/systemd/system/screen.service

echo "Enabling service and starting.."
systemctl daemon-reload
service screen start
service screen status

echo "Successfully Installed"
