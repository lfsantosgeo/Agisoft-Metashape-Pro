# -*- coding: utf-8 -*-
"""
Created on Thu May 10 14:00:47 2018
@author: luiz fernando dos santos

This script produces a CSV file listing the source and estimated heights
for each camera in active chunk. By changing the code th horizontal coordinates
can be assessed (X, Y).

"""

# import the necessary modules to work with Python
import PhotoScan as PS                # Agisoft PhotoScan module

# Identify Agisoft PhotoScan version
ps_version = PS.app.version
print("Camera Height Script")
print("---------------------------------------------------------------------\n"
      "Running on Agisoft PhotoScan {}".format(ps_version))

# Checking compatibility
compatible_major_version = "1.4"
found_major_version = ".".join(PS.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible PhotoScan version: {}"
                    " != {}".format(found_major_version,
                                    compatible_major_version))
print("Compatible version of script!\n"
      "---------------------------------------------------------------------\n"
      "\nScript started!\n")

# Image quality report
path_cam = PS.app.getExistingDirectory("Specify export folder:")
path_cam += "/Camera_Height.csv"

global doc  # defining doc a global variable everywhere in the function!
doc = PS.app.document  # current document project in PS
chunk = doc.chunk  # current definition of chunk in PS

labels = []
e_hlist = []
s_hlist = []
for camera in chunk.cameras:
    if camera.transform:  # just for the aligned cameras
        labels.append(camera.label)
        # estimated value of Z
        estimated = chunk.crs.project(chunk.transform.matrix.mulp(camera.center))
        e_hlist.append(estimated.z)
        # source (measured) value of Z
        measured = camera.reference.location
        s_hlist.append(measured.z)

lists = [labels, e_hlist, s_hlist]

# creates the csv file based on the camera list
with open("F:\XUBUNTU\SHARED_FOLDER\Batch2\Camera_Height.csv", "w",
          newline="") as myfile:
    myfile.write("List of ALIGNED CAMERAS with the respective Z values\r\n")
    myfile.write("\n")
    myfile.write("LABEL\t\tSOURCE\t\tESTIMATE\r\n")
    for row in zip(*lists):
        myfile.write("{}\t{:.2f}\t\t{:.2f}\r\n".format(*row))

print("Done! CSV file generated!\n"
      "Available at {}".format(path_cam))
print("---------------------------------------------------------------------"
      "\n")
