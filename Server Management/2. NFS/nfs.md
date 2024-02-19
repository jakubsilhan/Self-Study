# Instalace
Instalace nfs serveru.  
`apt install nfs-kernel-server`  
Vytvořil jsem si adresář /srv/nfs.  
`mkdir /srv/nfs`

# Úprava konfigurace
Pro úpravu konfigurace jsem použil nano.  
`nano /etc/exports`  
Přidal jsem zde řádek povolující přístup ze serveru "zihadlo". Pracoval jsem pouze s tímto serverem, protože jsem si navzájem s Pavlem vyzkoušeli, zda vše funguje.  
`/srv/nfs jina.adresa.cz(rw,sync,no_root_squash,subtree_check)`  
Je nutné zmínit, že pro možnost zapisovat přes nfs, je nutné specifikovat no_root_squash, které dovoluje rootovi z klienta do složky na serveru zapisovat  
`exportfs -a `  
Po dokončení úprav konfigurace je bylo potřeba ještě exportovat. To proběhlo bez problémů.  
`showmount -e`  
Použitím příkazu showmount jsem si zobrazil své exporty.  

# Nastavení firewall
Pro umožnění přístupu jsem ještě nastavil výjimku pro nfs ve firewall z vymezené sítě.  
`ufw allow from xxx.xxx.x.x/16 to any port nfs`

# Klient na serveru
Nejdříve jsem nainstaloval klienta.  
`apt install nfs-common`  
Poté jsem si připravil složku kam namountuji přístup na k jinemu serveru.  
`mkdir /opt/jiny_server`  
Zde jsem namountoval jiny server.  
`mount jina.adresa.cz:/srv/nfs /opt/jiny_server`  
To samé jsem provedl pro perun.  
`mkdir /opt/perun`  
`mount dalsi.adresa.cz:/srv/nfs /opt/perun`  
Zde se nacházel soubor zvire.txt s obrázkem šneka.