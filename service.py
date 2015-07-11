#Modules General
import lightpack

# Modules XBMC
import xbmc, xbmcgui, xbmcaddon

###########################################################

__addon__ = xbmcaddon.Addon("service.lightpackage")
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__settings__ = __addon__
__language__ = __settings__.getLocalizedString

lpack = lightpack.lightpack(__settings__.getSetting("host"), int(__settings__.getSetting("port")), __settings__.getSetting("apikey"), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
startUpMode = __settings__.getSetting("usage")

###########################################################


def log(msg):
    LOGDEBUG = 2
    message = '%s: %s' % (__settings__.getAddonInfo("name"), msg)
    if __settings__.getSetting("debug") == "true":
            level = LOGDEBUG
            xbmc.log(message, level)

def notification(text):
    text = text.encode('utf-8')
    icon = __settings__.getAddonInfo("icon")
    smallicon = icon.encode("utf-8")
    if __settings__.getSetting("notification") == "true":
        xbmc.executebuiltin('Notification(Lightpack,'+text+',3000,' + smallicon + ')')

def setProfile(enable, profile):
    if enable:
        xbmc.sleep(300)
        lpack.lock()
        lpack.turnOn()
        lpack.setProfile(profile)
        lpack.unlock()
    else:
        log('Trying to set profile but is disable')
        lpack.turnOff()


def playingARLessThan(nAR):
    xbmc.sleep(200)
    pAR = float(round(xbmc.RenderCapture().getAspectRatio(), 2))
    if pAR <= float(round(nAR, 2)):
        return True
    else:
        return False

def typeMediaPlayingIS(mType):
    xbmc.sleep(200)
    if xbmc.Player().isPlayingVideo() and mType == "video":
        log('Currently media playing is video')
        return True
    elif xbmc.Player().isPlayingAudio() and mType == "audio":
        log('Currently media playing is audio')
        return True
    else:
        return False

class Main:

    def __init__(self):
        self.Player = LightPlayer()
        # add code to try to catch if lightpack/prismatik is installed if not exit service,
        # try code already on lpack.connect check lightpack.py
        if startUpMode == '0' and __settings__.getSetting("default_enable") == "true":
            xbmc.sleep(200)
            log('Active while Kodi is running')
            lpack.connect()
            setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("default_profile"))
            lpack.disconnect()
        else:
            log('active while playing media only')

        while True:
            if xbmc.Monitor().waitForAbort(10):
                lpack.connect()
                lpack.lock()
                lpack.turnOff()
                lpack.unlock()
                lpack.disconnect()
                break


class LightPlayer(xbmc.Player):

    def __init__(self):
        xbmc.Player.__init__(self)

    def onPlayBackStarted(self):
        log('Playback started')
        lpack.connect()
        if typeMediaPlayingIS("video"):
            xbmc.sleep(500)
            currentAspectRatio = float(round(xbmc.RenderCapture().getAspectRatio(), 2))
            log('Detecting aspect ratio %s and setting the closest video profile available ' % currentAspectRatio)
            if playingARLessThan(1.33):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_1"))
            elif playingARLessThan(1.37):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_2"))
            elif playingARLessThan(1.66):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_3"))
            elif playingARLessThan(1.78):  # mine/default
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_4"))
            elif playingARLessThan(1.85):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_5"))
            elif playingARLessThan(2.20):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_6"))
            elif playingARLessThan(2.35):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_7"))
            elif playingARLessThan(2.40):  # mine
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_8"))
            elif playingARLessThan(2.55):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_9"))
            elif playingARLessThan(2.76):
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("video_profile_10"))
            else:
                setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("default_profile"))

        lpack.disconnect()

    def onPlayBackEnded(self):
        log('PlayBack stopped/ended')
        if startUpMode == '0':  # start with kodi
            xbmc.sleep(500)
            lpack.connect()
            setProfile(__settings__.getSetting("default_enable"), __settings__.getSetting("default_profile"))
            lpack.disconnect()

        if startUpMode == '1':  # start only with media
            xbmc.sleep(500)
            lpack.connect()
            lpack.lock()
            lpack.turnOff()
            lpack.unlock()
            lpack.disconnect()

    def onPlayBackStopped(self):
        self.onPlayBackEnded()


if __name__ == "__main__":
    print '%s - %s, has started ' % (__addonname__, __addonversion__)
    Main()
    print '%s - %s, has stopped' % (__addonname__, __addonversion__)
