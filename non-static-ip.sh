# 1. Copy original (non-static ip) files

echo "Copying original dhcpcd.conf, dnsmasq.conf and hostapd files"
sudo cp /etc/dhcpcd.conf.orig /etc/dhcpcd.conf
sudo cp /etc/dnsmasq.conf.orig /etc/dnsmasq.conf
sudo cp /etc/default/hostapd.orig /etc/default/hostapd

# 2. Stop, disable and mask hostapd

echo "stop, disable and mask hostapd"
sudo systemctl stop hostapd
sudo systemctl disable hostapd
sudo systemctl mask hostapd

# 3. Restart DHCP

echo "Restarting DHCP..."
sudo systemctl restart dhcpcd
