# Samba
Velkou část úlohy jsem dělal podle manuálu na stránkách Samby.
# Instalace
Nejdříve jsem sambu nainstaloval.  
*apt install samba*  
Následně jsem zkontroloval jestli běží  
*systemctl status smbd -> running*

# Firewall
Firewall jsem nastavil stejně jako pro FTP.  
*ufw allow from xxx.xxx.x.x/16 to any app 'Samba'* -> jen z vymezené sítě

# Kontrola konfigurace
*cat /etc/samba/smb.conf | grep "server role"* -> kontroluji, že je standalone server

# Uzivatel
Nejprve jsem si pro Sambu vytvořil adresář.  
*mkdir /srv/samba/*  
*chgrp sambashare /srv/samba/*  
Poté jsem vytvořil uživatele bez možnosti přihlášení.  
*sudo useradd -d /srv/samba/smbuser -s /usr/sbin/nologin -G sambashare smbuser*  
Byl problém, že se home adresář nevytvořil automaticky, takže jsem ho vytvořil manuálně.  
*mkdir /srv/samba/smbuser*  
*chown smbuser /srv/samba/smbuser*  
*chmod 755 /srv/samba/smbuser* -> práva jsem nastavil tak, aby mohl uživatel uploadovat i stahovat

Nakonec bylo potřeba uživatele pro Sambu aktivovat.  
*smbpasswd -a smbuser*  
*smbpasswd -e smbuser*

# Úprava konfigurace
Před úpravou jsem si vytvořil backup.  
*cp /etc/samba/smb.conf{,.backup}*  
Poté jsem na konec konfigurace vložil informace o uživateli smbuser.  
*nano /etc/samba/smb.conf*
```
[smbuser]
    path = /srv/samba/smbuser
    browseable = no
    read only = no
    force create mode = 0660
    force directory mode = 2770
    valid users = smbuser
```

Pro aktualizaci konfigurace jsem ještě musel restartovat daemony  
*systemctl restart smbd*
*systemctl restart nmbd*

# Zkouška
Jelikož používám systém windows, tak jsem si v prohližeči souborů přidal akorát svůj server. Musel jsem vyplnit údaje a nakonec jsem se úspěšně přihlásil.  
Adresa pro přihlášení byla: \\\adresa.cz\smbuser

Přes command line jsem vytvořil ve složce soubor pokus.txt.  
*nano /srv/samba/smbuser/pokus.txt* -> Ten jsem viděl.

Po chvilce experimentování s právy jsem poté přes Windows zkusil vytvořit další soubor.
To když jsem provedl, tak jsem si v command line zkusil příkaz ls a druhý soubor jsem zde viděl.

Tím jsem došel k závěru, že vše funguje správně.