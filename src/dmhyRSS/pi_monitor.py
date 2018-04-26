# -*- coding: utf-8 -*-
# main process : check pi state, run TorrentCollect and omxplay
import time
import os
import control as cl
import RPi.GPIO as GPIO
import torrent_collect

debug = 0

class PiMonitor(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP) # shutdown button
        GPIO.setup(11,GPIO.OUT, initial = 0) # Fan control
        GPIO.add_event_detect(3, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)
        self.torrent_runnning = 0

    def run(self):
        cl.open_omxplay_gui()
        self.torrent = TorrentCollect()
        self.torrent_runnning = torrent.run()
        while True: # every 1m =30 s
            try:
                if self.torrent_runnning == 1:
                    self.check_harddisk_spare()
                else:
                    pass
                self.check_HDMI_status()
                self.control_CPU_GPU_tempture()
                time.sleep(1*20)
            except Exception as 'HDD space full': 
                self.torrent.close()
                self.torrent_runnning = 0
            else:
                self.torrent.close()
                raise
                
    def check_harddisk_spare(self):
        spare = cl.check_HDD_spare()
        if debug:
            print spare
        if spare < 1.0:
            raise Exception('HDD space full')
        else:
            pass

    def check_HDMI_status(self):
        status = cl.check_HDMI_status()
        if debug:
            print status

    def control_CPU_GPU_tempture(self):
        CPU_temp = cl.Check_CPU_tempture()
        GPU_temp = cl.Check_GPU_tempture()

        if debug:
            print CPU_temp
            print GPU_temp

        if CPU_temp > 50.0 or GPU_temp >50.0:
            GPIO.output(11,1)
        elif CPU_temp < 45.0 and GPU_temp < 45.0:
            GPIO.output(11,0)
        else:
            pass

def Shutdown(channel):
    os.system("sudo shutdown -h now")


if __name__ == '__main__':
    app = PiMonitor()
    app.run()