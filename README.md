# 39-Inf-NP-Abschlussprojekt
Abschlussprojekt: Modulbezeichnung "39-Inf-NP Netzwerkprogrammierung", Universität Bielefeld: Technische Fakultät


# Projektbeschreibung
Im Rahmen dieses Projekts soll eine Client-/ Serverlösung für so genannte ThinClients entwickelt werden. Diese soll die Verwaltung und Administration der Clients implementieren. 

# ThinClients
Basieren auf dedizierter Hardware und sind äußerst Energiesparend.
Da es keine beweglichen Teile - wie Lüfter - gibt, sind sie äußerst Robust. 
Sie bieten wenig bis keine Erweiterungsoptionen.
ThinClients verfügen über Standard I/O Anschlüsse.
Es besteht die Möglichkeit ein minimalistisches Unix System auszuführen. Dazu gehören bspw. Tiny Core, Igel OS, etc.

# Motivation
Heutzutage betreiben viel große Unternehmen eigene Server oder mieten solche. Wenn es darum geht große Datenmengen berechnen 
zu wollen wird oft Mals die Rechenleistung von Servern genutzt. Die technische Ausstattung von Arbeitsplätzen ist teuer. Die Auslastung der Server oft gering. Es würde sich daher anbieten, Arbeitsplätze mit günstiger Hardware - den ThinClients - zu bestücken, die eine remote Verbindung zum Server ermöglichen. Implizit würden Serverkapazitäten so optimal genutzt und die Kosten für Arbeitsplatzeinrichtungen reduziert.


# Ziel
Eine Client-/ Serverlösung für so genannte ThinClients. Diese implementiert nach Möglichkeit folgende Features:
1) Heartbeat
2) Update
3) Upgrade

# Anforderungen 
Die formalen Projektanforderungen definieren sich wie folgt:
1) Projektdokumentation auf GitHub
2) Implementierung in Python 3
3) Dokumentation in Pydoc
4) Diese Projektbeschreibung in Markdown (Usage, Beispiel)


# USAGE
Clone this repo to a directory on your device.

Make sure that Flask is installed.
Type "pip3 install Flask"

# USAGE: ThinClient_server

Inside the directory run:

export FLASK_APP=thinClient_server
export FLASK_ENV=development
flask run

This will start the server.

# USAGE: ThinClient_client
