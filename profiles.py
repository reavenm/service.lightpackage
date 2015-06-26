
#Modules General
import os,lightpack
from sys import argv

# Modules XBMC
import xbmc, xbmcgui, xbmcaddon

__language__ = __settings__.getLocalizedString
#########################################################################################################
## BEGIN
#########################################################################################################
lpack = lightpack.lightpack(__settings__.getSetting("host"), int(__settings__.getSetting("port")), __settings__.getSetting("apikey"), [1,2,3,4,5,6,7,8,9,10] )
lpack.connect()
menu = lpack.getProfiles()
del menu[-1]
menu.append(__language__(32071))
off = len(menu)-1
quit = False
while not quit:
	selected = xbmcgui.Dialog().select(__language__(32070), menu )
	if selected!= -1:
		lpack.lock()
		if (off==int(selected)):
			lpack.turnOff()
		else:
			lpack.turnOn()
			lpack.setProfile(menu[selected])
		lpack.unlock
	quit = True
lpack.disconnect()