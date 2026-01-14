# game_server_fastapi

Der aktuelle Stand des GameServers, so wie gezeigt im Seminar. 

- nahezu keine Fehlerbehandlung
- hart codierte Beschränkungen (max 8 User, nach 100 Ticks wird eine Message gelöscht)
- die Route "/all" dient der Diagnose ... hier werden einfach alle aktuellen Nachrichten geliefert
- über die Route /ws kann eine (zusätzliche) WebSocket Connection aufgebaut werden
  - clients können darüber broadcast messages an alle weiteren verbundenen WebSockets schicken
  - unter /wstest is ein sehr einfacher Websocket-Chat umgesetzt
  - über den WebSocket werden die ticks des game servers verschickt    


Viel Spass beim Ausprobieren

LG JTM
