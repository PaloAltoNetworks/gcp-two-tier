#!/bin/bash
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1
while true
  do
   resp=$(curl -s -S -g --insecure "https://10.5.2.4/api/?type=op&cmd=<show><chassis-ready></chassis-ready></show>&key=LUFRPT1CU0dMRHIrOWFET0JUNzNaTmRoYmkwdjBkWWM9alUvUjBFTTNEQm93Vmx0OVhFRlNkOXdJNmVwYWk5Zmw4bEs3NjgwMkh5QT0=")
   if [[ $resp == *"[CDATA[yes"* ]] ; then
     break
   fi
  sleep 10s
done
apt-get update
apt-get install -y apache2 wordpress
ln -sf /usr/share/wordpress /var/www/html/wordpress
gzip -d /usr/share/doc/wordpress/examples/setup-mysql.gz
while true
 do
  resp=$(mysql -udemouser -ppaloalto@123 -h 10.5.3.2 -e 'show databases')
  if [[ $resp == *"Demo"* ]]; then
     break
  fi
 sleep 5s
done
exit
bash /usr/share/doc/wordpress/examples/setup-mysql -n Demo -t ",{"Fn::GetAtt" : [ "WPDBServerInstance", "PrivateIp" ]}," ",{"Fn::GetAtt" : [ "WPDBServerInstance", "PrivateIp" ]},"
sed -i \"s/define('DB_USER'.*/define('DB_USER', 'demouser');/g\" /etc/wordpress/config-",{"Fn::GetAtt" : [ "WPDBServerInstance", "PrivateIp" ]},".php
sed -i \"s/define('DB_PASSWORD'.*/define('DB_PASSWORD', 'paloalto@123');/g\" /etc/wordpress/config-",{"Fn::GetAtt" : [ "WPDBServerInstance", "PrivateIp" ]},".php
mv /etc/wordpress/config-",{"Fn::GetAtt" : [ "WPDBServerInstance", "PrivateIp" ]},".php /etc/wordpress/config-",{ "Ref": "PublicElasticIP" },".php
wget -O /usr/lib/cgi-bin/guess-sql-root-password.cgi https://raw.githubusercontent.com/PaloAltoNetworks/aws/master/two-tier-sample/guess-sql-root-password.cgi
chmod +x /usr/lib/cgi-bin/guess-sql-root-password.cgi
sed -i \"s/DB-IP-ADDRESS/",{"Fn::GetAtt" : [ "WPDBServerInstance", "PrivateIp" ]},"/g\" /usr/lib/cgi-bin/guess-sql-root-password.cgi
wget -O /usr/lib/cgi-bin/ssh-to-db.cgi https://raw.githubusercontent.com/PaloAltoNetworks/aws/master/two-tier-sample/ssh-to-db.cgi
chmod +x /usr/lib/cgi-bin/ssh-to-db.cgi
sed -i \"s/DB-IP-ADDRESS/",{"Fn::GetAtt" : [ "WPDBServerInstance", "PrivateIp" ]},"/g\" /usr/lib/cgi-bin/ssh-to-db.cgi
wget -O /var/www/html/sql-attack.html https://raw.githubusercontent.com/PaloAltoNetworks/aws/master/two-tier-sample/sql-attack.html
ln -sf /etc/apache2/conf-available/serve-cgi-bin.conf /etc/apache2/conf-enabled/serve-cgi-bin.conf
ln -sf /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load
systemctl restart apache2
