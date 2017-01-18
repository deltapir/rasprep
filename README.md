#timelapse.py

Per usare **timelapse.py** basta fare un file `conftimelapse.txt` nella stessa cartella dell'applicazione e scriverci *latitudine* e *longitudine* 
dell'`observer` (cioè da dove si vuole osservare la Luna (*per ora*) dalla Terra).

`40.0000:20.00000:`

Prima la *latitudine* e poi la *longitudine*!

**Stat'v bbuon, waju!**


#Futuri implementi in timelapse.py

- [x]  Aggiungere la letture da un file `conftimelapse.txt` delle latitudini dell'observer;
- [x]  Aggiungere una riga che si sovrascrive quando il programma calcola il 
	tempo `lapse` per la `moon2`;
- [ ]  Sistemare in generale l'output del programma;
- [ ]  Aggiungere un semplice `body-follower` che indica continuamente la posizione
	del pianeta/satellite/stella;
- [ ]  Tradurre il programma in inglese;
- [x]  Aggiornare il file `readmetimelapse.md` per la visualizzazione su [GitHub](www.github.com); 
- [x]  Incorporare il file `futuretimelapse.md` in `readmetimelapse.md`;
- [ ]  Universalizzare **timelapse.py** per renderlo funzionante con qualsiasi oggetto
	`epheem.body` da importare da `conftimelapse.txt`;
- [ ]  Supporto Telegram-Bot;
- [ ]  Aggiunta di personalizzazioni del programma da chiedere al primo avvio:
 - [ ]  Nome utente;
 - [ ]  Coordinate dell'observer;
 - [ ]  `epheem.body` da seguire;

