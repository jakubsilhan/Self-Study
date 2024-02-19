# Instalace Docker
Nejdříve bylo potřeba zprovoznit docker. Začal jsem aktualizací databáze balíčků.  
`apt update`  
Nejdříve jsem nainstaloval baličky potřebné pro instalaci Dockeru.  
`apt install apt-transport-https ca-certificates curl software-properties-common`  
Poté jsem si stáhl a uložil GPG klíč pro ověřování integrity docker balíčků.  
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`  
Přidal jsem si Docker repozitář do systémového repozitáře dostupných balíčků.  
`echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`  
Ještě jednou jsem si aktualizoval databázi balíčků s již nově přidaným dockerem.  
`apt update`  
Následně jsem zkontroloval jakou verzi budu vlastně instalovat.  
`apt-cache policy docker-ce`  
A nainstaloval jsem docker.  
`apt install docker-ce`  
Poté jsem zkontroloval zda běží a zkusil jsem příkaz spustit image hello-world pro kompletní jistotu.  
`systemctl status docker`  
`docker run hello-world`  

```
root@adresa:~# docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
719385e32844: Pull complete
Digest: sha256:c79d06dfdfd3d3eb04cafd0dc2bacab0992ebc243e083cabe208bac4dd7759e0
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

# Java 8
S funkčním dockerem jsem se rozhodl zprovoznit javu 8.  
`docker run -it --name java8-container openjdk:8-jdk bash`  
Tady jsem vždy musel kontejner znovu spustit, jelikož jsem se nejdřív objevil v kontejnerovém bash, který když jsem opustil, tak se kontejner zastavil.  
`docker start java8-container`  
Následně jsem zkontroloval verzi javy.  
`docker exec -it java8-container java -version`  
Poté jsem si vytvořil jednoduchý skript pro javu.  
`nano /usr/local/bin/HelloWorld.java`  
```
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```
Ten jsem musel dostat do samotného kontejneru.  
`docker cp /usr/local/bin/HelloWorld.java java8-container:/root/`  
Nakonec jsem skript pro kontrolu spustil.  
`docker exec -it java8-container bash -c "javac /root/HelloWorld.java && java -cp /root HelloWorld"`  

```
root@adresa:~# docker exec -it java8-container bash -c "javac /root/HelloWorld.java && java -cp /root HelloWorld"
Hello, World!
```
Po dokončení práce jsem kontejner zastavil.  
`docker stop java8-container`  
A ověřil jsem si, že je opravdu zastavený.  
`docker ps -a`  

# Java 11
Instalace proběhla stejně.  
`docker run -it --name java11-container openjdk:11-jdk bash`  
Opět jsem kontejner musel spustit.  
`docker start java11-container`  
A otestoval jsem verzi.  
`docker exec -it java11-container java -version`  
Překopíroval jsem opět skript.  
`docker cp /usr/local/bin/HelloWorld.java java11-container:/root/`  
A nakonec jsem ho pro kontrolu opět spustil.  
`docker exec -it java11-container bash -c "javac /root/HelloWorld.java && java -cp /root HelloWorld"`  

```
root@adresa:~# docker exec -it java11-container bash -c "javac /root/HelloWorld.java && java -cp /root HelloWorld"
Hello, World!
```
Kontejner bylo potřeba také zastavit.  
`docker stop java11-container`

Vše se mi tedy nakonec podařilo zprovoznit.