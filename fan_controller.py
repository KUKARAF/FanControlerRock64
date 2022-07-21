import os
import importlib
import sys
import datetime
import argparse

pathPWM = "/sys/devices/platform/pwm-fan/hwmon/hwmon2/pwm1"
pathTEMP = "/sys/class/thermal/thermal_zone0/temp"
pathLOG = sys.path[0] + "fan_controller.log"
tempMax = 60
tempMin = 40
minPWM = 60

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
    print( "Current CPU temperature: " + str(getTemp()/1000)+"C")

    try:
        value = int(pwm)
    except ValueError:
        raise
    if value < 0 or value > 255:
        raise ValueError("Expected 0 <= value <= 255, got value = " + format(value))
    else:
        with open(pathPWM, "w") as f:
            if pwm < minPWM and pwm > 0:
                f.write(str(minPWM))
                print("Fan set to minimum fan speed:" + str(round(minPWM/255*100)) + "% (fanPWM: " + str(minPWM) + ")")
            else:
                f.write(str(pwm))
                print("Fan set to:" + str(round(pwm/255*100)) + "% (fanPWM: " + str(pwm) + ")")

def checkForceRange(arg):
    try:
        value = int(arg)
    except ValueError as err:
       raise argparse.ArgumentTypeError(str(err))
    if value < 0 or value > 100:
        message = "Expected 0 <= value <= 100, got value = {}".format(value)
        raise argparse.ArgumentTypeError(message)
    return value

parser = argparse.ArgumentParser()
parser.add_argument("--min", help="Fan will only go on above set temperature. Default: 40C")
parser.add_argument("--max", help="Temperature from which fan speed will be maximum. Default: 60C")
parser.add_argument("-l", "--log", default="fan.log", help="Log to file. Default: fan.log.")
parser.add_argument("-f", "--force", type=checkForceRange, metavar="[0-100]", help="Set a static fan speed, values from 0-100")

args = parser.parse_args()

if not len(sys.argv) > 1:
    writeFanPWM(tempToPWM())
elif args.force is not None:
    writeFanPWM(percentToPWM(args.force))
elif args.log:
    logNow()