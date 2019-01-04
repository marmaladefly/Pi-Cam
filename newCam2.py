import datetime as dt

from time import sleep

from picamera import PiCamera

import picamera



class Tymers:

    def __init__(self):
        self.t = dt.datetime.now()
        self.day = self.t.strftime('%d')
        self.hour = self.t.strftime('%H') 
        self.minute = self.t.strftime('%M')
        self.second = self.t.strftime('%S')
        self.dta = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


tNow = Tymers()

stick = ["USB2", "USB101", "USB102","USB103","USB106", "D999-4B3D"]       #list of usb sticks to be used

halfcount = 1

for g in range(1, 960):                                                  # 1000 half hour limit loop

    ind = int (halfcount/160)                                             # 160 half hours per usb stick
    st = stick[ind]

    print(g," half hours recorded  ", halfcount, " files on drive   ",st, "  no of drives used", ind)   
    # tNow = Tymers()
    
    h = int(tNow.hour)
    m = int(tNow.minute)
    s = int(tNow.second)

    if m < 30:
        half = "A"
    else:
        half = "B"

    hc = tNow.day + tNow.hour+half

    camera = PiCamera(resolution=(1280, 720))

    if h > 17 or h < 7:                                                   # night time hours settings

        
        camera.iso = 800
        camera.exposure_mode = 'night'
        camera.framerate = 6
        

    else:
        camera.exposure_mode = 'auto'

    sleep(20)

    try:
        camera.start_recording("/media/pi/%s/mvid%s.h264" %( st , hc))    # need to put a try clause in for next section
        
        print( tNow.day," day of month.  Hour ", tNow.hour, "  ",half)
            
        counter = 1
        
        while counter == 1:
            disp = dta = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.annotate_text = disp
            sleep(1)

            tNow = Tymers()
            m = int(tNow.minute)
            s = int(tNow.second)

            if m == 29 and s > 58:
                counter = 0
                print("End of half hour")

            else:
                counter = 1

            if m == 59 and s > 58:

                counter = 0

                print(" End of Hour ")


        sleep(2)

        camera.stop_recording()

        print("recording file ended   ")

        camera.close()

        tNow = None                                                          # nullify the get a new time reading

        tNow = Tymers()                                                      # these two lines may not be needed


        halfcount = halfcount + 1

    except:

        print ("error ocurred")

print("prog ended ")
