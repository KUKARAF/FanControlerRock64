import os
import importlib
import sys
import datetime
import argparse

pathPWM = "/sys/devices/platform/pwm-fan/hwmon/hwmon2/pwm1"
pathTEMP = "/sys/class/thermal/thermal_zone0/temp"
pathLOG = sys.path[0] + "fan.log"
tempMax = 70
tempMin = 35


def getTemp():
    with  open(pathTEMP, "r") as f:
        temp = int(f.read().replace('\n',''))
        return temp
def getPWM(p=pathPWM):
    with open(p,'r') as f:
        return f.readlines()[0].replace('\n','')

def logNow():
    with open(pathLOG,'a') as f:
        f.write("temp: "+str(getTemp())+ " fanPWM: "+str(getPWM())+" date: "+ str(datetime.datetime.now()) + "\n")
def tempToPWM(t=getTemp()/1000,mi=tempMin,ma=tempMax,maxPWM=255):
    if t>ma:
        return maxPWM
    elif t<mi:
        return 0
    else:
        return ((t/mi)-1)*maxPWM
def percentToPWM(p):
    return round(255/100*p)

def writeFanPWM(pwm):
    with open(pathPWM, "w") as f:
        f.write(str(150))

    if pwm > 255 or pwm < 0:
        raise ValueError('only values in range 0-255 allowed')
    else:
        with open(pathPWM, "w") as f:
            if pwm < 60 and pwm>0:
                f.write(str(60))
                print("set fan to "+str(round(60/255.0*100))+"%")
            else:
                f.write(str(pwm))
                print("set fan to "+str(round(pwm/255.0*100))+"%")
            print( "temperature at "+ str(getTemp()/1000)+" C")

def argparseLoad():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", help="Static fan speed, values from 0-100")
    parser.add_argument("--max", help="Static fan speed, values from 0-100")
    parser.add_argument("-l", "--log", help="Static fan speed, values from 0-100")
    parser.add_argument("-f", "--force", type=int, choices=list(range(0, 101)), help="Static fan speed, values from 0-100")

if __name__ == "__main__":

    argparseLoad()

    writeFanPWM(tempToPWM())
    if  len(sys.argv) > 1:
        if sys.argv[1] == 'force':
            print("Reason: user specified")
            writeFanPWM(percentToPWM(int(sys.argv[2])))

    logNow()
