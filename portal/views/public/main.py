from django.http import HttpResponseRedirect
from django.shortcuts import *
from django.template import RequestContext
from django.shortcuts import render
from django import forms
from django.shortcuts import redirect
from django.utils.encoding import smart_unicode, smart_str
import subprocess
import re, time
from portal.libs.apsettings import makehostapdfile
import os, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


class APsettings(object):

	def __init__(self, ssid, passphrase, channel, securitytype, encrypttype):
		self.ssid = "SAIFE-INE"
		self.passphrase = "saife123"
		self.channel = 1
		self.securitytype = "WPA"
		self.encrypttype = "TKIP"


def mainview(request):
    return HttpResponseRedirect('/dashboard')

def dashboard(request):

	try:
		pifstat =  int(subprocess.check_output(['pidof', 'saife_connect']))
	except subprocess.CalledProcessError as e:
		pifstat = e.returncode
	if pifstat == 1:
		status = 'Not Running'
	else:
		status = 'Running'
	return render(request, 'public/dashboard.html',{'status': status} )




def APconfig(request):
	
	APsettings1 = APsettings(0,0,0,0,0)

	#makehostapdfile("breck","is", "super", "/home/breck/SC2.0/hostapd.conf.org", "/home/breck/SC2.0/hostapd.conf" )
	currentsettings = subprocess.check_output(['cat','/home/breck/SC2.0/hostapd.conf'])
	print(currentsettings)
	APsettings1.ssid = re.search('\nssid=(.+)', currentsettings).group(1)
	APsettings1.passphrase = re.search('\passphrase=(.+)', currentsettings).group(1)
	APsettings1.channel = re.search('\channel=(.+)', currentsettings).group(1)

	print(APsettings1.ssid)

	if request.method == "POST":
		#print('hello')
		ssid = (request.POST['ssid'])
		passwds = (request.POST['passwds'])
		channel = (request.POST['chan'])
		#print(request.POST['secType'])
		#print(request.POST['encrypt'])

		makehostapdfile(ssid,passwds,channel, "/home/breck/SC2.0/hostapd.conf.org", "/home/breck/SC2.0/hostapd.conf" )


		message = "Setting Have Been Updated"



	return render_to_response('public/APconfig.html',{}, context_instance=RequestContext(request))

def tunnel(request):

	csr = subprocess.check_output(['cat','/home/breck/SC2.0/.SaifeConnectClient/newkey.smcsr'])
	key = re.search('<csr>(.*)<\/csr>', csr).group(1)


	return render(request, 'public/tunnel.html',{'key': key})



	

class ConStats(object):

	
	def __init__(self, ip, subnet, mac, rx, tx):
		self.ip = ip
		self.subnet = subnet
		self.mac = mac
		self.rx = rx
		self.tx = tx


class ConStatsAll(object):

	
	def __init__(self, eth0, cectun, wlan0):
		self.eth0 = ConStats(0,0,0,0,0)
		self.cectun = ConStats(0,0,0,0,0)
		self.wlan0 = ConStats(0,0,0,0,0)	



def getstats(dev):

	iface = ConStats(0,0,0,0,0)

	try:
		stats = subprocess.check_output(['ifconfig',str(dev)])
	
		iface.ip = re.search('inet addr:([0-9.]+)', stats)
		if iface.ip:
			iface.ip = iface.ip.group(1)

		iface.subnet = re.search('Mask:([0-9.]+)', stats)
		if iface.subnet:
			iface.subnet = iface.subnet.group(1)

		iface.mac = re.search('HWaddr ([0-9a-f:]+)', stats)
		if iface.mac:
			iface.mac = iface.mac.group(1)

		iface.rx = re.search('RX packets:(\d+)', stats)
		if iface.rx:
			iface.rx = iface.rx.group(1)


		iface.tx = re.search('TX packets:(\d+)', stats)
		if iface.tx:
			iface.tx = iface.tx.group(1)
	except:
		pass

	return iface



def connections(request):

	statsAll = ConStatsAll(0,0,0)
	statsAll.eth0 = getstats('eth0')
	statsAll.cectun = getstats('CEC_TUN0')
	statsAll.wlan0 = getstats('wlan0')
	return render(request, 'public/connections.html',{'statsAll': statsAll} )

def advance(request):


	return render(request, 'public/advance.html')

class Car(object):

	def __init__(self, name, color):
		self.name = name
		self.color = color


		

def home(request):
	if request.method == 'POST':
		ssid = request.POST.get('ssid')
		return render(request, 'public/home.html', {'ssid': ssid})

	elif request.method == 'GET':
		cars = [Car('bmw', '#848484'), Car('lambo', '#FFFF00')]
		return render(request, 'public/home.html', {'cars': cars})



def getlog(request):
	filename = smart_str('/home/breck/SC2.0/saife_connect.log.0604.0')# Select your file here.                                
	wrapper = FileWrapper(file(filename))
	response = HttpResponse(wrapper, content_type='text/plain')
	response['Content-Length'] = os.path.getsize(filename)

	return response


def enable(request):
	awk_sort = subprocess.Popen( "sudo -S sh /home/breck/SC2.0/bin/saife_connect_console.sh &", stdin=subprocess.PIPE, shell=True )
	awk_sort.communicate( b"bcB1173a\n" )
	time.sleep(3)
	return redirect('/dashboard')

def disable(request):

	awk_sort = subprocess.Popen( "sudo -S pkill -2 saife_connect", stdin=subprocess.PIPE, shell=True )
	awk_sort.communicate( b"bcB1173a\n" )
	time.sleep(3)
	return redirect('/dashboard')

def passthrough(request):

	return redirect('/dashboard')
