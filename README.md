# RockPro64 Cooling Fan Controller

Forked from: KUKARAF/FanControlerRock64

Python script to control fan on a Pine64 RockPro64 single board computer. 

## Installation

```
mkdir fan_controller
wget https://raw.githubusercontent.com/kromsam/FanControlerRockPro64/master/fan_controller.py -O fan_contr
oller/fan_controller.py
python fan_controller.py
```

## Usage

### Automatic mode

Enables fan if temp between tempMax = 70 and  tempMin = 35 where tempMax is 100% fan speed and tempMin is 23%.

```python enable_fan.py```

### Static mode

Static fan speed to desired strengh 0-100:

```python ebable_fan.py force 90```
