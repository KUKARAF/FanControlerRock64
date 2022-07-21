import os
import importlib
import sys
import datetime
import argparse

def check100Range(arg):
    try:
        value = int(arg)
    except ValueError as err:
       raise argparse.ArgumentTypeError(str(err))
    if value < 0 or value > 100:
        message = "Expected 0 <= value <= 100, got value = {}".format(value)
        raise argparse.ArgumentTypeError(message)
    return value

def getTemp():
    with  open(pathTEMP, 'r') as f:
        temp = int(f.read().replace('\n',''))
        return temp / 1000

def getPWM():
    with open(pathPWM,'r') as f:
        return f.readlines()[0].replace('\n','')

def logNow():
    with open(pathLOG,'a') as f:
        f.write(str(datetime.datetime.now()) + "Temperature: " + str(getTemp()) + "C - fanPWM: " + str(getPWM()) + "\n")

def tempToPWM():
    t = getTemp()
    if t >= tempMax:
        return maxPWM
    if t < tempMin:
        return 0
    return round(maxPWM / (tempMax - tempMin) * (t - tempMin))

def percentToPWM(p):
    return round(p / 100 * maxPWM)

def pwmToPercent(p):
    return round(p / maxPWM * 100)

def writeFanPWM(pwm):
    print( "Current temperature: " + str(getTemp())+"C")
    try:
        value = int(pwm)
    except ValueError:
        raise
    if value < 0 or value > maxPWM:
        raise ValueError("Expected 0 <= value <= " + maxPWM + ", got value = " + format(value))
    else:
        with open(pathPWM, "w") as f:
            if pwm < minPWM and pwm > 0:
                f.write(str(minPWM))
                print("Fan set to minimum fan speed: " + str(pwmToPercent(minPWM)) + "% (fanPWM: " + str(minPWM) + ")")
            else:
                f.write(str(pwm))
                print("Fan set to: " + str(pwmToPercent(pwm)) + "% (fanPWM: " + str(pwm) + ")")

parser = argparse.ArgumentParser()
parser.add_argument("--min", type=int, help="Fan will only switch on above set temperature threshold. Default: 40C.")
parser.add_argument("--max", type=int, help="Fan speed will be maximum above set temperature. Default: 60C.")
parser.add_argument("-l", "--log", nargs='?', default="fan_controller.log", help="Log to a file, setting filepath is optional. Default: 'fan_controller.log' in same folder as 'fan_controller.py'.")
parser.add_argument("-f", "--force", type=check100Range, metavar="[0-100]", help="Set a static fan speed, values from 0-100.")
parser.add_argument("--minpwm", type=check100Range, metavar="[0-100]", help="Set minimum fan speed. Default: 24 percent (fanPWM: 60).")
parser.add_argument("--gpu", action="store_true", help="Use GPU temperature instead of CPU temperature.")

args = parser.parse_args()

pathPWM = "/sys/devices/platform/pwm-fan/hwmon/hwmon2/pwm1"
maxPWM = 255

if args.gpu:
    pathTEMP = "/sys/class/thermal/thermal_zone1/temp"
else:
    pathTEMP = "/sys/class/thermal/thermal_zone0/temp"

if args.log:
    pathLOG = args.log
else:
    pathLOG = sys.path[0] + "/fan_controller.log"

if args.min is not None:
    tempMin = int(args.min)
else:
    tempMin = 40

if args.max is not None:
    tempMax = int(args.max)
else:
    tempMax = 60

try:
    tempMin > tempMax
except:
    raise ValueError("Minimum temperature can't be higher than maximum temperature.")

if args.minpwm is not None:
    minPWM = percentToPWM(args.minPWM)
else:
    minPWM = 60

if args.force is not None:
    writeFanPWM(percentToPWM(args.force))
else:
    writeFanPWM(tempToPWM())

if args.log:
    logNow()