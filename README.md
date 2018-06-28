# 1. 39-Inf-NP-Abschlussprojekt
Abschlussprojekt: Modulbezeichnung "39-Inf-NP Netzwerkprogrammierung", Universität Bielefeld: Technische Fakultät

Siehe [Projektbeschreibung des Veranstalters](http://bibiserv.cebitec.uni-bielefeld.de/resources/lehre/netprog18/Projekt-2018.pdf)

### 1.1 Projektbeschreibung
Im Rahmen dieses Projekts soll eine Client-/ Serverlösung für so genannte ThinClients entwickelt werden. Diese soll die Verwaltung und Administration der Clients implementieren. 

### 1.2 ThinClients
Basieren auf dedizierter Hardware und sind äußerst Energiesparend.
Da es keine beweglichen Teile - wie Lüfter - gibt, sind sie äußerst Robust. 
Sie bieten wenig bis keine Erweiterungsoptionen.
ThinClients verfügen über Standard I/O Anschlüsse.
Es besteht die Möglichkeit ein minimalistisches Unix System auszuführen. Dazu gehören bspw. Tiny Core, Igel OS, etc.

### 1.3 Motivation
Heutzutage betreiben viel große Unternehmen eigene Server oder mieten solche. Wenn es darum geht große Datenmengen berechnen 
zu wollen wird oft Mals die Rechenleistung von Servern genutzt. Die technische Ausstattung von Arbeitsplätzen ist teuer. Die Auslastung der Server oft gering. Es würde sich daher anbieten, Arbeitsplätze mit günstiger Hardware - den ThinClients - zu bestücken, die eine remote Verbindung zum Server ermöglichen. Implizit würden Serverkapazitäten so optimal genutzt und die Kosten für Arbeitsplatzeinrichtungen reduziert.


### 1.4 Ziel
Eine Client-/ Serverlösung für so genannte ThinClients. Diese implementiert nach Möglichkeit folgende Features:
1) Heartbeat
2) Liste der bekannten Clients
3) Informationen zu jedem Client
4) Upgrade: Installation von Paketen (Hier .zip Dateien)
5) Update: Update von bereits installierten Paketen

#### 1.5 Anforderungen 
Die formalen Projektanforderungen definieren sich wie folgt:
1) Projektdokumentation auf GitHub
2) Implementierung in Python 3
3) Dokumentation in Pydoc
4) Diese Projektbeschreibung in Markdown (Usage, Beispiel)

# 2. Umsetzung

**- - T O D O - -**

### 2. Beispiel

**- - T O D O - -**

# 3. USAGE

Clone this repo to a directory on your device.

Make sure that Flask is installed

- pip3 install Flask

## 3.1 USAGE: ThinClient_server

### 3.1.1 Development Environment

Inside the top directory of '/thinClient_server' run

- export FLASK_APP=thinClient_server 
- export FLASK_ENV=development

Initialize the database by running

- flask init-db

Now you can run the flask server by running

- flask run

This will start the server in debug mode.

### 3.1.2 Real Usage

Inside the top directory of '/thinClient_server' run

- export FLASK_APP=thinClient_server

Initialize the database by running:

- flask init-db

Now you can run the flask server by running:

- flask run

This will start the server.

## 3.2 USAGE: ThinClient_client

Inside where ever you copy the client script run

- chmod a+x thinClient_client.py

You can than start the client shell with

- ./thinClient_client.py

##### Note

If you would like to change the installation directory change the global variable in thinClient_client.py
