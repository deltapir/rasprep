#!/usr/bin/python
from __future__ import print_function
from time import sleep
import time
import sys
import RPi.GPIO as GPIO
import ephem
import math
import ConfigParser
config=ConfigParser.RawConfigParser()
import os

GPIO.setmode(GPIO.BOARD) #conta i pin sulla board

ControlPin = [7,11,13,15] #vettore dei pin

for pin in ControlPin: 
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,0)

seq = [ [0,0,0,1], #matrice halfstep per la rotazione oraria
        [0,0,1,1],
        [0,0,1,0],
        [0,1,1,0],
        [0,1,0,0],
        [1,1,0,0],
        [1,0,0,0],
        [1,0,0,1] ]

GPIO.setwarnings(False)
GPIO.cleanup()

def INTERO (int):			#rotazione di 45 gradi albero interno
	for i in range(int):         
		FRAZIO (8)

def FRAZIO (res):
	global pin, ControlPin, seq
	GPIO.setmode(GPIO.BOARD)
	for pin in ControlPin:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,0)
	for halfstep in range(res):  #rotazione ciclo frazionato a 5.625 per ciclo dell'albero interno e di 5.625/64 dell'albero esterno
                for pin in range(4):
                        GPIO.output(ControlPin[pin], seq[halfstep][pin])
                        #print (ControlPin[pin], seq[halfstep][pin])
                time.sleep(0.001)
	GPIO.cleanup()

def FIRST(moon2az): #ruota il motore alla posizione iniziale
	print ("INIZIO PROGRAMMA FIRST")
        moon2az=((float(moon2az)*180)//3.1415)	#da radianti in gradi
	pinint=int(((moon2az*64)//(5.625*8))) 		#numero di step da 5.625*8 dell'albero interno per effettuare la rotazione dell'albero esterno
	pinint8=pinint			
	pinres=int(((moon2az*64)//(5.625))-pinint*8) #numero di pin rimanenti
	print ("GIRI COMPLETI ", pinint8)
        print ("GIRI FRAZ ", pinres)
	#raw_input ("Premi INVIO per eseguire il Ciclo INTERO!")
	print ("INIZIO Ciclo INTERO!")
	INTERO(pinint8)
	print ("FINE Ciclo INTERO!")
	#raw_input ("Premi INVIO per eseguire il Ciclo FRAZIONATO!")
	print ("INIZIO Ciclo FRAZIONATO!")
	FRAZIO (pinres)
	print ("FINE Ciclo FRAZIONATO!")
	#raw_input ("FINE FIRST")

def COMPUTE (lon, lat, moon, moon2, reflex, reflexvirt):
	#print ("Funzione COMPUTE!")
	data = DATA()
	reflex.date = data
        reflexvirt.date = data
        moon.compute(reflex)
        moon2.compute(reflexvirt)
        monalt = ephem.degrees(moon.alt)
        #print(str(monalt))
	monaz = ephem.degrees(moon.az)
        #print (str(monaz))
	mon2alt = ephem.degrees(moon2.alt)
        #print (str(mon2alt))
	mon2az = ephem.degrees(moon2.az)
	#print (str(mon2az))
	return (monalt, monaz, mon2alt, mon2az)

def DATA():
	dat = ephem.Date(time.strftime('%Y/%m/%d %H:%M:%S'))-ephem.hour #ephem vuole l'ora in UTC
	#print ('stampo la data dentro DATA() ', dat)
	return dat

def POS(body): return body.alt, body.az

def CONFIG():
	conftime=open('conftime.ini','w')
	config.add_section('User')
        name=raw_input("Inserisci il tuo nome: ")
        config.set('User','Name',name)
        config.add_section('Observer')
        lats=raw_input("Inserisci la latitudine dell'observer: ")
        config.set('Observer','lats',lats)
        long=raw_input("Inserisci la longitudine dell'observer: ")
        config.set('Observer','long',long)
        config.write(conftime)
        conftime.close()

#####################################################	MAIN	#####################################################	#######################################
#create a INI file for configparsers
if os.path.isfile('./conftime.ini')==True:			#cerca il file conftime.ini
	conftime = open("conftime.ini",'r+')			#se lo trova lo apre
	config.readfp(conftime)					#lo legge
	if config.has_section('User')== True:			#se ha la sezione 'User' scritto dentro
		print("Benvenuto %s. La tua longitudine e latitudine sono: %s - %s" % (config.get('User','Name'), config.get('Observer','long'), config.get('Observer','lats')))
		conftime.close()
	else:							
		conftime.close()				#se non e' scritto dentro
		CONFIG()		
else:								#se non trova il file conftime.ini
	print("Sei sccemo")					
	CONFIG()
		
print (time.strftime("Oggi e il %d/%m/%Y e sono le %H:%M:%S")) 
a = raw_input("Giusto? ") 
if a.startswith('n'):
        print ("Devi cambiare l'ora manualmente: riprova")
        print ("\n\n                     RICORDA")
        print ("||sudo cp -p /usr/share/zoneinfo/Europe/Rome /etc/localtime per la timezone")
        print ("||")
        print ("||sudo ntpdate -u ntp1.ien.it per l'ora esatta")
        print ("||")
        sys.exit() 
raw_input ("Quando sei pronto, premi INVIO! \n")

#read from conftime.ini
lat=config.get('Observer','lats')
lon=config.get('Observer','long')

#lapse=input("Tempo tra uno scatto e l'altro? ")
#wait=input("Tra quanti secondi inizia il time-lapse? ")

reflex = ephem.Observer()    #definisco due observer per le due lune moon e moon2
reflexvirt = ephem.Observer()
reflex.lon = lon
reflexvirt.lon = lon
reflex.lat = lat
reflexvirt.lat = lat
reflex.elevation = 49
reflexvirt.elevation = 49

moon=ephem.Moon()
moon2=ephem.Moon()

moonalt, moonaz, moon2alt, moon2az = COMPUTE (lon, lat, moon, moon2, reflex, reflexvirt)
FIRST (moon2az)
#sleep(wait)
while 1<5:
	i=0
	a=ephem.degrees(0.0015339) 	#tutti gli angoli in pyephem sono in radianti
	#a=ephem.degrees(0.01)		#usato solo per provare con tempi minori
	#print (a)
	moonalt, moonaz, moon2alt, moon2az = COMPUTE(lon, lat, moon, moon2, reflex, reflexvirt)
	while (abs((ephem.degrees(moonalt))-(ephem.degrees(moon2alt))) <= a ) and (abs((ephem.degrees(moonaz))-(ephem.degrees(moon2az)))<=a): #dico che la differenza di azimut e altitudine delle due lune deve essere inferiore
		moonalt, moonaz, moon2alt, moon2az = COMPUTE (lon, lat, moon, moon2, reflex, reflexvirt)		#al passo del motore
		#print(abs(moon2az-moonaz))    	
		#print("Azimut2: ", moon2az)   	#stampa l'azimut di moon2
		#print("Azimut: ", moonaz)     	#stampa l'azimut di moon
		#print(a)    		      	#stampa l'angolo
		#print i                       	#stampa l'iterazione ovvero i secondi da aspettare
		#print
		data = DATA()		#mi restituisce l'ora e data del rasp
		reflexvirt.date = ephem.Date(data)+i*ephem.second 	#sposta l'ora di osservazione di moon2
		#print('Stampo la data dentro il while ', reflexvirt.date)
		moon2.compute(reflexvirt)				#computa la posizione di moon2 con la nuova ora
		moon2az=str(moon2.az)		#restituisce l'azimut in angolo di moon2
		moon2alt=str(moon2.alt)
		print('Tra ',i,' secondi la luna sta in AZ:',moon2az,'e ALT:',moon2alt, end='\r')
		#raw_input ("INVIO")
		#moon2.compute(reflexvirt)
		lapse = i			#aggiorno il time di lapse tra uno scatto e l'altro
		i+=1
	FRAZIO (8)
	print('\n')
	print ('Bisogna aspettare ',lapse,' secondi ')	
	#print('%f %f' % (moonaz, moonalt))     <--RIPRISTINALO
	print("Posizione moon2 tra ",lapse," secondi: ", moon2az,"e ",moon2alt)
	print("Posizione moon attuale: ", moonaz,"e ",moonalt)
	sleep(lapse)

GPIO.cleanup()
