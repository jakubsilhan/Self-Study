# Upload skriptu
Zde jsem opět využil již nainstalované samby. Poté jsem akorát skript přesunul do správného adresáře.  
`mv /srv/samba/smbuser/fakt.php /var/www/html/fakt.php`  
Zde jsem zjistil, že není nainstalované php. Zobrazil se přímo kód. Tak jsem php nainstaloval.  
`apt install php`  
Následně už byl skript spustitelný na adrese:  
`http://adresa.cz/fakt.php?cislo=300000`.  

# Stress testing
Nejdříve jsem si nainstaloval modul pro stress testing.  
`apt install stress`  
Když jsem spustil stress pouze pro zátěž procesoru, tak se žádná velká změna nekonala.  
`stress --cpu  8 --timeout 20`  
Zkusil jsem také zpustit jak php tak python skript najednou. Zde se konalo zpomalení php skriptu, které trvalo někdy až dvojnásobek výchozího času.  

Následně jsem zkusil virtual memory stress test. Zde se zátěž také projevila. Místo běžných 0.7s už proces trval okolo 1.4s. Pro tuto zátěž jsem použil příkaz:  
`sudo stress --vm 8 --timeout 20s`  
Z tohoto soudím, že rychlost skriptu je ovlivněna virtuální pamětí a ne zátěží procesoru.

# Instalace Python
Nejdřív jsem si nebyl jist, zda byl nainstalovaný python.  
`apt install python3`  
Zde jsem si potvrdil, že instalovaný již byl. A jen jsem si ověřil verzi.  
`python3 --version`  
Následně jsem musel aktivovat modul cgi (Common Gateway Interface), aby mohl externí program přistupovat k http requestům.  
`a2enmod cgi`  
Pak byl potřeba restart Apache.  
`systemctl restart apache2`  
Pro skripty jsem si poté vytvořil dedikovanou složku.  
`mkdir /var/www/html/scripts`  
Pro složku jsem v konfiguraci nastavil použití cgi pro všechny soubory s koncovkou .py. Provede je jako cgi skript.  
`nano /etc/apache2/apache2.conf`  
```
<Directory /var/www/html/scripts>
        Options +ExecCGI
        AddHandler cgi-script .py
</Directory>
```
Poté jsem si vytvořil v této složce jednoduchý skript, který byl podobný fakt.php.  
`nano /var/www/html/scripts/test.py`  
Zde jsem trochu bojoval a Apache mi i několikrát padl. Proto se hodilo kouknout do Apache logu.  
`cat /var/log/apache2/error.log`  
Tam jsem zjistil, že v python skriptu nesmím zadat příliš velké číslo, jinak skript padne. Tento skript byl mnohem pomalejší než php. Spustit tento skript lze na adrese:  
`adresa.cz/scripts/test.py?cislo=20000`
