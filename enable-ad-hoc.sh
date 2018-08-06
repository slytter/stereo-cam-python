
read -p "Change to ad-hoc (or back to wifi) ? " -n 1 -r 
if [[ $REPLY =~ ^[Yy]$ ]]
then
	echo "Changing to ad-hoc"
	sudo bash -c "cat interface_configs/ad-hoc > /etc/network/interfaces"
	sudo ifup wlan0
else
	echo"Changing to normal wifi"
	sudo bash -c "cat interface_configs/wifi > /etc/network/interfaces"
fi


read -p "Restart this Pi?" -n 1 -r 
if [[ $REPLY =~ ^[Yy]$ ]]
then
	echo "Restarting"
	sudo shutdown -r 0
else
	echo "Not restarting"
fi

