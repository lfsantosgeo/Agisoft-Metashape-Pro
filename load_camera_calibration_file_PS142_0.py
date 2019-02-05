# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 10:56:19 2019

@author: Luiz Fernando dos Santos

PhotoScan Pro Version 1.4.2
"""

import PhotoScan as PS

app = PS.app
doc = app.document  # current document project in PS
chunk = doc.chunk  # current definition of chunk in PS

sensor = chunk.sensors[0]  # direct changes to sensor [0]
print("Calibration file loading to sensor:", chunk.sensors[0])
if not sensor.width and sensor.height:
    sensor.width = chunk.cameras[0].photo.image().width
    sensor.height = chunk.cameras[0].photo.image().height
else:
    print("Sensor already have height and width information!")
calib = PS.Calibration()

path_lens = PS.app.getOpenFileName("Add your Agisoft"
                                   " PhotoScan Lens"
                                   " Calibration file:", "*.xml;*.XML")
print("LENS CALIBRATION FILE:\n", path_lens)
try:
    calib.load(path_lens, format="xml")
    print("Loading Camera Calibration file into PhotoScan...")
except OSError:
    print("There is no specified path to file!")
    raise

sensor.calibration = calib  # set the Adjusted tab values according to file
sensor.user_calib = calib  # set the Initial tab values according to file

"""
If very precise calibration data is available, to protect it from
recalculation one should check Fix calibration box. In this case initial
calibration data will not be changed during Align Photos process.

[True]: To protect the calibration data from being refined during Align Photos
process one should check Fix calibration box on the Initial tab for the chunk
with the data to be processed. In this case initial calibration values will
not be changed during Align Photos process.

[False]: Initial calibration data will be adjusted during the Align Photos
processing step. Once Align Photos processing step is finished adjusted
calibration data will be displayed on the Adjusted tab of the Camera
Calibration dialog box. Using all aerial images available might improve the
camera calibration parameters further (f, cx, cy, b1, b2, k1-k4, p1-p4) by
reestimating and refining them based on the lens calibration initial
calculated data.
"""
sensor.fixed = False
