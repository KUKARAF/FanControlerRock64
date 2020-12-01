# FanControlerRock64

simple fan controller for the ROCK64 pine single board computer. 

installation: 
save *.py file and create chrontab to run regularly 
write permission might have to be enabled for /sys/class/hwmon/hwmon0/pwm1 

Usage: 
automatic mode, enables fan if in specified values:

python enable_fan.py 

Static fan speed to desired strengh 0-100:

python ebable_fan.py force 90  
