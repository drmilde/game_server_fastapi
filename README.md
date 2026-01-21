# game_server_fastapi

Der aktuelle Stand des GameServers, so wie gezeigt im Seminar. 

- nahezu keine Fehlerbehandlung
- hart codierte Beschränkungen (max 8 User, nach 100 Ticks wird eine Message gelöscht)
- die Route "/all" dient der Diagnose ... hier werden einfach alle aktuellen Nachrichten geliefert
- über die Route /ws kann eine (zusätzliche) WebSocket Connection aufgebaut werden
  - clients können darüber broadcast messages an alle weiteren verbundenen WebSockets schicken
  - unter /wstest ist ein sehr einfacher Websocket-Chat umgesetzt
  - über den WebSocket werden die ticks des game servers verschickt

## Ticks

Ticks werden über den Websocket an alle verbundenen Clients versendet. Die erfolgt bei folgenden Aktionen/Endpunkten
  - Hinzufügen eines User über /j
  - Versenden einer Nachricht über /s/{id}/{r}
  - Dem Abrufen von Nachrichten über /m/{id}

Als Nachricht wird ein String mit folgender Syntax verschickt: 
  - "tick: 19", also
  - Das Schlüsselwort "tick" gefolgt von ":" als Trennzeichen, gefolgt von dem Stand des tick-counters als int-Wert


Viel Spass beim Ausprobieren

LG JTM
