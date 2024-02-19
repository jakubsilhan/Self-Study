# Instalace
Nainstaloval jsem Lynis.  
`apt update`  
`apt install lynis`  

Provedl jsem audit  
`lynis audit system`  
-> Hardening index : 65

# Oprava SMTP
Mezi warningy byla chyba u SMTP. Tu jsem opravil.  
```
Found some information disclosure in SMTP banner (OS or software name) [MAIL-8818] https://cisofy.com/lynis/controls/MAIL-8818/
```
`nano /etc/postfix/main.cf`  
```
mtpd_banner = $myhostname ESMTP
```
`/etc/init.d/postfix restart`  

# Úprava ssh konfigurace
Hlavní úpravou byla změna konfigurace SSH. Zde jsem provedl několik změn, které Hardening index ovlivnily nejvíce.  
```
 Consider hardening SSH configuration [SSH-7408]
    - Details  : AllowTcpForwarding (set YES to NO)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : ClientAliveCountMax (set 3 to 2)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : Compression (set YES to NO)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : LogLevel (set INFO to VERBOSE)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : MaxAuthTries (set 6 to 3)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : MaxSessions (set 10 to 2)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : TCPKeepAlive (set YES to NO)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : X11Forwarding (set YES to NO)
      https://cisofy.com/lynis/controls/SSH-7408/

  * Consider hardening SSH configuration [SSH-7408]
    - Details  : AllowAgentForwarding (set YES to NO)
      https://cisofy.com/lynis/controls/SSH-7408/
```
Naštěstí jsem se poté stále přihlásil.  
# Instalace Malvare scanneru
Pro lepší zabezpečení jsem nainstaloval malware scanner.  
`apt install rkhunter`    

# Úprava postfixu
Lynis mě upozornil na další chybu v postfixu.  

```
Disable the 'VRFY' command [MAIL-8820:disable_vrfy_command]
    - Details  : disable_vrfy_command=no
    - Solution : run postconf -e disable_vrfy_command=yes to change the value
      https://cisofy.com/lynis/controls/MAIL-8820/
```
`postconf -e disable_vrfy_command=yes`  


# Úprava login.defs
Lynis také doporučil úpravu souboru login.defs.  
```
  * Configure minimum password age in /etc/login.defs [AUTH-9286]
      https://cisofy.com/lynis/controls/AUTH-9286/

  * Configure maximum password age in /etc/login.defs [AUTH-9286]
      https://cisofy.com/lynis/controls/AUTH-9286/

  * Default umask in /etc/login.defs could be more strict like 027 [AUTH-9328]
      https://cisofy.com/lynis/controls/AUTH-9328/
```

`nano /etc/login.defs`  
```
PASS_MIN_DAYS 7
PASS_MAX_DAYS 90
UMASK 027
```

# Instalace zobrazování verzí
Zde se jedná o další doporučení Lynisu.  
`apt install apt-show-versions`

# Poslední kontrola
Provedl jsem poslední audit systému.  
`lynis audit system`  
```
  Hardening index : 74 [##############      ]
  Tests performed : 275
  Plugins enabled : 1
```