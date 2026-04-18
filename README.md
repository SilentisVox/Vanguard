# Vanguard

Vanguard is an open source, cross platform **Command & Control** framework.
It can help organizations of all sizes to practice security testing.
The primary purpose of **Vanguard** is to stage and manage TCP connections.
It was made with the **HACK5: USB Rubber Ducky** strictly in mind.
This makes it a very important tool for penetration testers and offsensive security practitioners.

[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.6-yellow.svg)](https://www.python.org/)
<img src="https://img.shields.io/badge/Developed%20on-Windows%2011-1677CF">
[![License](https://img.shields.io/badge/License-BSD%203%20Clause%20license-C91515)](https://github.com/SilentisVox/Silence/blob/master/LICENSE)
<img src="https://img.shields.io/badge/Maintained%3F-Yes-1FC408">

### Features

- Interactive CLI
- Argument Parsing for Configuration
- TCP/HTTP Stager
- Payload Generation
- Session Management Commands
- Service Control Commands
- Utility Commands
- Core Client-Side Payload
- Colorized Output and Formatting

### Setup

```
git clone https://github.com/SilentisVox/Vanguard
cd Vanguard
python3 vanguard.py
```

### Usage

```
 → python vanguard.py -h

usage: vanguard.py [-h] [-c CALLBACK] [-tp TCP_PORT] [-hp HTTP_PORT] [-q]

options:
  -h, --help                             show this help message and exit
  -c  CALLBACK,  --callback CALLBACK     Callback address.
  -tp TCP_PORT,  --tcp-port TCP_PORT     TCP listen port.
  -hp HTTP_PORT, --http-port HTTP_PORT   HTTP listen port.
  -q, --quiet
```

```
Vanguard> help

help

 Command        Description
 --------------------------------------------------------------

 start     [+]  Starts a given service with parameters.
 kill      [+]  Kills a given service.
 generate  [+]  Generates a payload to the handler specified.
 options        Displays current services running.
 sessions       Displays all sessions with clients.
 session   [+]  Begin communication with a given client.
 end       [+]  Kills a connection with a specified client.
 eradicate      Kills all current sessions.
 help      [+]  Displays this menu or command details.
 clear          Clears the terminal window.
 exit           Exits Vanguard.
```