
read -p "Change to ad-hoc (or back to wifi) ? " -n 1 -r 
if [[ $REPLY =~ ^[Yy]$ ]]
then
	printf "\n - Changing to ad-hoc \n"
	sudo bash -c "cat interface_configs/ad-hoc > /etc/network/interfaces"
	sudo ifdown wlan0 --force
	sudo ifup wlan0 --force

else
	printf "\n - Changing to normal wifi \n"
	sudo bash -c "cat interface_configs/wifi > /etc/network/interfaces"
fi


read -p "Restart this Pi?" -n 1 -r 
if [[ $REPLY =~ ^[Yy]$ ]]
then
	printf "\n - Restarting \n"
	sudo reboot now
else
	printf "\n - Not restarting \n"
fi

