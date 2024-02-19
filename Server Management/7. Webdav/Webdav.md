# Instalace Webdav
Zde stačilo akorát zprovoznit moduly v apachi.  
`a2enmod dav`  
`a2enmod dav_fs`  
Poté jsem jen restartoval apache.  
`systemctl restart apache2.service`  

# Konfigurace Webdav
Nejdříve jsem si připravil prostředí pro webdav.  
`mkdir /var/www/webdav`  
`chown www-data:www-data /var/www/webdav`  

`mkdir -p /usr/local/apache/var/`  
`chown www-data:www-data /usr/local/apache/var`  

Poté jsem upravil konfiguraci přidáním řádku DavLock a přidáním webdav directory a aliasu.   
`nano /etc/apache2/sites-enabled/adresa-le-ssl.conf`
```
DavLockDB /usr/local/apache/var/DavLock
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerAdmin moje.jmeno@email.cz
    ServerName adresa.cz
    ServerAlias www.adresa.cz
    DocumentRoot /var/www/html/adresa
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    SSLCertificateFile /etc/letsencrypt/live/adresa.cz/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/adresa.cz/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf

    Alias /webdav /var/www/webdav

    <Directory /var/www/webdav>
        DAV On
    </Directory>
</VirtualHost>
</IfModule>
```
Poté jsem jen zkontroloval správný syntax v konfiguraci.  
`apachectl configtest`  
A restartoval jsem apache
`systemctl restart apache2.service`  
Pro kontrolu jsem se připojil pomocí Windows File Exploreru.  

# Autentizace
Dále jsem chtěl zprovoznit přihlašování do webdavu. Proto jsem si nejdříve připravil soubor pro uložení hesla.  
`touch /usr/local/apache/var/users.password`  
`chown www-data:www-data /usr/local/apache/var/users.password`  
Následně jsem přidal uživatele kubix.  
`htdigest /usr/local/apache/var/users.password webdav kubix`  
Nakonec jsem opět upravil konfiguraci tak, aby vždy požadovala přihlášení pro přístup do složky webdav.  
`nano /etc/apache2/sites-enabled/adresa-le-ssl.conf`  
```
<Directory /var/www/webdav>
  DAV On
  AuthType Digest
  AuthName "webdav"
  AuthUserFile /usr/local/apache/var/users.password
  Require valid-user
</Directory>
```
Zapnul jsem autorizaci uživatele.  
`a2enmod auth_digest`  
A restartoval jsem apache.  
`systemctl restart apache2.service`  

Nakonec jsem otestoval připojení pomocí několika způsobů:  
Nejdříve jse použil Windows File Explorer, který byl jednoduchý na zprovoznění a dost intuitivní.  
Následně jsem vyzkoušel WinSCP, se kterým již mám zkušenost a byl již nainstalovaný. Zde tedy také nebyl žádný problém.  
Nakonec jsem si nainstaloval Cyberduck, který byl podobný WinSCP.  
Všechny klienty se mi podařilo zprovoznit bez větších problémů, ale trochu mě zarazilo, jak rozdílné mohou být v maličkostech, které však zabrání připojení.  
Pomocí všech klientů se mi podařilo pracovat se složkou webdav na mém virtuálu.

# Owncloud
Nainstaloval jsem si bez problémů klienta a po vyplnění přihlašovacích údajů jsem úspěšně propojil klienta s cloudem.  
Řekl bych, že Owncloud je přístupností nejpodobnější Windows File Exploreru. Ostatní klienti vždy požadují spuštění a přihlášení, zatímco owncloud se chová jako další připojený disk. V porovnání s OneCloudem od Windows mi přišel dost podobný a zatímco Google Disk je velmi užitečný nástroj, postrádá Google takové propojení se souborovým systémem.
