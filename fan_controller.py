''' controls fan speed on RockPro64 single board computer '''


import sys
import datetime
import argparse


def check_range_0_100(arg):
    ''' checks if argument is integer between 0 and 101 '''
    try:
        value = int(arg)
    except ValueError as err:
        raise argparse.ArgumentTypeError(str(err))
    if value < 0 or value > 100:
        message = "Expected 0 <= value <= 100, got value = " + str(value)
        raise argparse.ArgumentTypeError(message)
    return value


def get_temp():
    ''' gets temperature from hwmon, converts it to degrees celsius '''
    with open(TEMPPATH, 'r', encoding="utf-8") as file:
        temperature = int(file.read().replace('\n', ''))
        return temperature / 1000


def get_pwm():
    ''' gets current PWM of fan '''
    with open(PWMPATH, 'r', encoding="utf-8") as file:
        return file.readlines()[0].replace('\n', '')


def log_now():
    ''' appends a logline to a logfile'''
    with open(LOGPATH, 'a', encoding="utf-8") as file:
        file.write(str(datetime.datetime.now()) + " - Temperature: " +
                str(get_temp()) + "C - fanPWM: " + str(get_pwm()) + "\n")


def temperature_to_pwm():
    ''' returns a PWM value for a given temperature '''
    temperature = get_temp()
    if temperature >= TEMPMAX:
        return PWMMAX
    if temperature < PWMMIN:
        return 0
    return round(PWMMAX / (TEMPMAX - TEMPMIN) * (temperature - TEMPMIN))


def percentage_to_pwm(percentage):
    ''' converts percentage to PWM value'''
    return round(percentage / 100 * PWMMAX)


def pwm_to_percentage(pwm):
    ''' converts PWM value to percentage'''
    return round(pwm / PWMMAX * 100)


def write_to_pwm(pwm):
    ''' checks PWM value, writes it to pwmfile and prints an output'''
    print("Current temperature: " + str(get_temp())+"C")
    try:
        value = int(pwm)
    except ValueError as err:
        raise ValueError() from err
    if value < 0 or value > PWMMAX:
        raise ValueError("Expected 0 <= value <= " + PWMMAX +
                         ", got value = " + format(value))
    with open(PWMPATH, 'w', encoding="utf-8") as file:
        if PWMMIN > pwm > 0:
            file.write(str(PWMMIN))
            print("Fan set to minimum fan speed: " +
                  str(pwm_to_percentage(PWMMIN)) + "% (fanPWM: " + str(PWMMIN) + ")")
            return
        file.write(str(pwm))
        print("Fan set to: " + str(pwm_to_percentage(pwm)) +
                  "% (fanPWM: " + str(pwm) + ")")


parser = argparse.ArgumentParser()
parser.add_argument(
    "--min", type=int,
        help="Fan will only switch on above set temperature threshold. Default: 40C.")
parser.add_argument(
    "--max", type=int, help="Fan speed will be maximum above set temperature. Default: 60C.")
parser.add_argument("-l", "--log", action="store_true",
                    help="Log to a file. Set path with '--path'.")
parser.add_argument("-p", "--path",
                    help="Set path of logfile. Default: 'fan_controller.log' in folder as script.")
parser.add_argument("-f", "--force", type=check_range_0_100,
                    metavar="[0-100]", help="Set a static fan speed, values from 0-100.")
parser.add_argument("--minpwm", type=check_range_0_100,
                    metavar="[0-100]",
                    help="Set minimum fan speed. Default: 24 percent (fanPWM: 60).")
parser.add_argument("--gpu", action="store_true",
                    help="Use GPU temperature instead of CPU temperature.")

args = parser.parse_args()

PWMPATH = "/sys/devices/platform/pwm-fan/hwmon/hwmon2/pwm1"
PWMMAX = 255

if args.gpu:
    TEMPPATH = "/sys/class/thermal/thermal_zone1/temp"
else:
    TEMPPATH = "/sys/class/thermal/thermal_zone0/temp"

if args.path:
    LOGPATH = args.path
else:
    LOGPATH = str(sys.path[0]) + "/fan_controller.log"

if args.min is not None:
    TEMPMIN = int(args.min)
else:
    TEMPMIN = 40

if args.max is not None:
    TEMPMAX = int(args.max)
else:
    TEMPMAX = 60

try:
    TEMPMIN > TEMPMAX
except ValueError as exc:
    raise ValueError(
        "Minimum temperature can't be higher than maximum temperature.") from exc

if args.minpwm is not None:
    PWMMIN = percentage_to_pwm(args.minpwm)
else:
    PWMMIN = 60

if args.force is not None:
    write_to_pwm(percentage_to_pwm(args.force))
else:
    write_to_pwm(temperature_to_pwm())

if args.log:
    log_now()
