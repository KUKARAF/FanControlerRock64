# FanControlerRock64

simple fan controller for the ROCK64 pine single board computer. 

installation: 
save *.py file and create chrontab to run regularly 
write permission might have to be enabled for /sys/class/hwmon/hwmon0/pwm1 

Usage: 
automatic mode, enables fan if temp between tempMax = 70 and  tempMin = 35 where tempMax is 100% fan speed and tempMin is 23% 

```python enable_fan.py       

Static fan speed to desired strengh 0-100:

```python ebable_fan.py force 90```
