
#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2022, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
# Notice
#   1. Changes to this file on Studio will not be preserved
#   2. The next conversion will overwrite the file with the same name
"""
import sys
import time
import datetime
import threading

"""
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
# git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
# cd xArm-Python-SDK
# python setup.py install
"""
from xarm import version
from xarm.wrapper import XArmAPI

print('xArm-Python-SDK Version:{}'.format(version.__version__))

arm = XArmAPI('192.168.1.220')
arm.clean_warn()
arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)
time.sleep(1)

params = {'speed': 100, 'acc': 2000, 'angle_speed': 20, 'angle_acc': 500, 'events': {}, 'variables': {}, 'quit': False}


# Register error/warn changed callback
def error_warn_change_callback(data):
    if data and data['error_code'] != 0:
        arm.set_state(4)
        params['quit'] = True
        print('err={}, quit'.format(data['error_code']))
arm.register_error_warn_changed_callback(error_warn_change_callback)


# Register state changed callback
def state_changed_callback(data):
    if data and data['state'] == 4:
        if arm.version_number[0] >= 1 and arm.version_number[1] >= 1 and arm.version_number[2] > 0:
            params['quit'] = True
            print('state=4, quit')
arm.register_state_changed_callback(state_changed_callback)
params['speed'] = 1000
params['acc'] = 50000
params['angle_speed'] = 90
params['angle_acc'] = 1145
if arm.error_code == 0 and not params['quit']:
    arm.reset()
if arm.error_code == 0 and not params['quit']:
    if arm.set_servo_angle(angle=[-233.8, -60.2, -49.8, 99.2, 71.0, -50.6], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=False) < 0:
        params['quit'] = True
if arm.error_code == 0 and not params['quit']:
    if arm.set_servo_angle(angle=[-197.7, 26.1, -105.9, 60.1, -5.5, -106.0], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=False) < 0:
        params['quit'] = True
if arm.error_code == 0 and not params['quit']:
    if arm.set_servo_angle(angle=[-354.2, -37.9, -31.9, 216.2, 26.8, -359.9], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=True) < 0:
        params['quit'] = True
if not params['quit']:
    time.sleep(3)
if arm.error_code == 0 and not params['quit']:
    arm.reset()

# Define GPIO callback handle thread
class EventGPIOThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.alive = False
        self.values = {'tgpio': {'digital': [-1] * 2, 'analog': [-1] * 2},'cgpio': {'digital': [-1] * 8, 'analog': [-1] * 2}}
        self.tgpio_digital_callbacks = []
        self.tgpio_analog_callbacks = []
        self.cgpio_callbacks = []

    def run(self):
        self.alive = True
        while arm.connected and arm.error_code == 0 and not params['quit']:
            if len(self.tgpio_digital_callbacks) > 0:
                _, values = arm.get_tgpio_digital()
                if _ == 0:
                    for item in self.tgpio_digital_callbacks:
                        for io in range(2):
                            if item['io'] == io and eval('{} {} {}'.format(values[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['tgpio']['digital'][io], item['op'], item['trigger'])):
                                item['callback']()
                    self.values['tgpio']['digital'] = values
            if len(self.tgpio_analog_callbacks) > 0:
                _, values = arm.get_tgpio_analog()
                if _ == 0:
                    for item in self.tgpio_analog_callbacks:
                        for io in range(2):
                            if item['io'] == io and eval('{} {} {}'.format(values[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['tgpio']['analog'][io], item['op'], item['trigger'])):
                                item['callback']()
                    self.values['tgpio']['analog'] = values
            if len(self.cgpio_callbacks) > 0:
                _, values = arm.get_cgpio_state()
                if _ == 0:
                    digitals = [values[3] >> i & 0x01 if values[10][i] in [0, 255] else 1 for i in range(8)]
                    analogs = [values[6], values[7]]
                    for item in self.cgpio_callbacks:
                        if item['type'] == 'digital':
                            for io in range(8):
                                if item['io'] == io and eval('{} {} {}'.format(digitals[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['cgpio']['digital'][io], item['op'], item['trigger'])):
                                    item['callback']()
                        elif item['type'] == 'analog':
                            for io in range(2):
                                if item['io'] == io and eval('{} {} {}'.format(analogs[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['cgpio']['analog'][io], item['op'], item['trigger'])):
                                    item['callback']()
                    self.values['cgpio']['digital'] = digitals
                    self.values['cgpio']['analog'] = analogs
            time.sleep(0.1)

params['events']['gpio'] = EventGPIOThread()


# Define Contoller GPIO-5 DIGITAL is HIGH callback
def controller_gpio_5_digital_is_changed_callback_1():
    arm.register_state_changed_callback(state_changed_callback)
params['speed'] = 1000
params['acc'] = 50000
params['angle_speed'] = 90
params['angle_acc'] = 1145
if arm.error_code == 0 and not params['quit']:
    arm.reset()
if arm.error_code == 0 and not params['quit']:
    if arm.set_servo_angle(angle=[-233.8, -60.2, -49.8, 99.2, 71.0, -50.6], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=False) < 0:
        params['quit'] = True
if arm.error_code == 0 and not params['quit']:
    if arm.set_servo_angle(angle=[-197.7, 26.1, -105.9, 60.1, -5.5, -106.0], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=False) < 0:
        params['quit'] = True
if arm.error_code == 0 and not params['quit']:
    if arm.set_servo_angle(angle=[-354.2, -37.9, -31.9, 216.2, 26.8, -359.9], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=True) < 0:
        params['quit'] = True
if not params['quit']:
    time.sleep(3)
if arm.error_code == 0 and not params['quit']:
    arm.reset()

params['events']['gpio'].cgpio_callbacks.append({'type': 'digital', 'io': 5, 'trigger': 1, 'op': '==', 'callback': controller_gpio_5_digital_is_changed_callback_1})
if not params['events']['gpio'].alive:
    params['events']['gpio'].start()

# Main loop
while arm.connected and arm.error_code == 0 and not params['quit']:
    time.sleep(1)