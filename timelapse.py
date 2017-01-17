#!/usr/bin/python
from __future__ import print_function
from time import sleep
import time
import sys
import RPi.GPIO as GPIO
import ephem
import math

GPIO.setmode(GPIO.BOARD) #conta i pin sulla board

ControlPin = [7,11,13,15] #vettore dei pin

for pin in ControlPin: 
	GPIO.setup(pin,GPIO.OUT)
	GPIO.output(pin,0)

seq = [	[1,0,0,0], #matrice halfstep
	[1,1,0,0],
	[0,1,0,0],
	[0,1,1,0],
	[0,0,1,0],
	[0,0,1,1],
	[0,0,0,1],
	[1,0,0,1] ]

GPIO.setwarnings(False)
GPIO.cleanup()

def INTERO (int):	#rotazione INTERA
	for i in range(int):         #rotazione ciclo intero  a 5.625
		FRAZIO (8)

def FRAZIO (res):
	global pin, ControlPin, seq
	GPIO.setmode(GPIO.BOARD)
	for pin in ControlPin:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin,0)
	for halfstep in range(res):  #rotazione ciclo frazionato a 0.7
                for pin in range(4):
                        GPIO.output(ControlPin[pin], seq[halfstep][pin])
                        #print (ControlPin[pin], seq[halfstep][pin])
                time.sleep(0.001)
	GPIO.cleanup()

def FIRST(moon2az): #ruota il motore alla posizione iniziale
	print ("INIZIO PROGRAMMA FIRST")
        pinint=int((moon2az//5.625)) 		#numero di rotazioni complete del rotore (5.625 gradi)
	pinint8=pinint*8			
	pinres=int(((moon2az//0.7)-pinint)/64) 	#numero di pin rimanenti
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


#####################################################	MAIN	#####################################################	#######################################

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

print("Leggo dal file")
with open("conftimelapse.txt", "r") as tconf:
	for line in tconf:
		coor=line.split(":")
		lat,lon=coor[0],coor[1]
		lon=str(lon)
		lat=str(lat)
print("Lat: ",lat, "\nLong: ",lon)

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
print('moonalt ', moonalt)
print('moonaz ', moonaz)
print('moon2alt ', moon2alt)
print('moon2az ', moon2az)
FIRST (moon2az)
#sleep(wait)
while 1<5:
	i=0
	a=ephem.degrees(0.098175) #tutti gli angoli in pyephem sono in radianti
	print (a)
	moonalt, moonaz, moon2alt, moon2az = COMPUTE(lon, lat, moon, moon2, reflex, reflexvirt)
	while (abs(ephem.separation(POS(moon), POS(moon2))) <= a ):  	#dico che la differenza di azimut delle due lune deve essere inferiore 
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
		print ('Tra ',i,' secondi la luna sta in ',moon2az,' ', end='\r')
		#raw_input ("INVIO")
		#moon2.compute(reflexvirt)
		lapse = i			#aggiorno il time di lapse tra uno scatto e l'altro
		i+=1
	FRAZIO (8)
	print ('Bisogna aspettare ',lapse,' secondi ')	
	#print('%f %f' % (moonaz, moonalt))     <--RIPRISTINALO
	print("Azimut2: ", moon2az)
	print("Azimut: ", moonaz)
	sleep(lapse)

GPIO.cleanup()