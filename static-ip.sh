# 1. Copy original (non-static ip) files

echo "Copying original dhcpcd.conf, dnsmasq.conf and hostapd files"
sudo cp /etc/dhcpcd.conf.static_ip /etc/dhcpcd.conf
sudo cp /etc/dnsmasq.conf.static_ip /etc/dnsmasq.conf
sudo cp /etc/default/hostapd.static_ip /etc/default/hostapd

# 2. Restart DHCP

echo "Restarting DHCP..."
sudo systemctl restart dhcpcd

# 3. Unmask, enable and start hostapd

echo "Unmask, enable and start hostapd"
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

