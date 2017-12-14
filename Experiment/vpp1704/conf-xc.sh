echo "Setting Up interfaces"
sudo $SFLAG $BINS/vppctl -p $1 set int state TenGigabitEthernetb/0/1 up

sudo $SFLAG $BINS/vppctl -p $1 set int state TenGigabitEthernetb/0/0 up

echo "Setting Xconnect 1->0"
sudo $SFLAG $BINS/vppctl -p $1 set int l2 xconnect TenGigabitEthernetb/0/1 TenGigabitEthernetb/0/0
