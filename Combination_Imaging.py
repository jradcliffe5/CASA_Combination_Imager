######################################################################
#
# Combination_Imaging.py
#
#   Creates combination image of all arrays in CASA format
#
# Created Jack Radcliffe 13/10/2015
#           
# Usage:
#
#         casapy CombinationImaging.py([msfile,msfile2,etc])
#
# (I)Python Notes:
#
#    Nominally, the .py file needs to be in the same directory 
#    you are running casapy from.  If you want to put the source in a
#    different directory, then:
#
#    1) Set up a place where you will put your modules and point a 
#       variable at it, e.g.:
#         export CASAPYUTILS="~/src/python_mods/"
#    2) Then make sure ipython knows about it by putting:
#         ip.ex("sys.path.append(os.environ['CASAPYUTILS'])")
#       in your ~/.ipython/ipy_user_conf.py (under the main: block).
#
######################################################################
#Begin the script:

from os import listdir
import numpy as np
import average_freq_time_sm.py

try:
    import casac,os
except ImportError, e:
    print "failed to load casa:\n", e
    exit(1)
mstool = casac.homefinder.find_home_by_name('msHome')
ms = casac.ms = mstool.create()
tbtool = casac.homefinder.find_home_by_name('tableHome')
tb = casac.tb = tbtool.create()



def phaseshift() #function to phase shift all sets to the source of interest! (need source coords)

################################################
####Average in frequency and time###############
################################################
def average_freq_time(msName,smearingpc,theta) #function to average w.r.t to frequency and time to get adequate FoV of observations
#Inputs
'''
smearingpc = 10. #percentage smearing required
theta = 60. #radial distance to get desired smearing
msName = '' # name of the ms file to be averaged!
'''

#################################################

def concatvis() #concatenate all visibilities in the working directory

# need for loop for gaussian w scale weights
def scaleweights()

def imagecombo() # image the combined image -> return the weights to uniform!

def fitscube() # use images created to generate an image cube with the various angular resolutions.

##########################################
# VARIABLES IN MAIN SCRIPT
mslist = [] #list of .ms files in the current working directory
# USER DEFINED VARIABLES
coords = ['J2000 12h31m08.1 62d34m05.2'] # Coordinates for phase centres
##########################################

for file in listdir('./'):
    if file.endswith('.ms'):
        mslist.append(file)

for i in range(len(mslist)):
    print '###################################################################################'
    print 'Your measurement set ' + mslist[i] + 'will now be phase shifted to coordinates' + coords
    print '###################################################################################'
        phaseshift(mslist[i],coords)
        print 'It will now be averaged to 10pc smearing at 1arcmin'
        average_freq_time(file)

concat(vis=mslist,concatvis='combined_%s.ms'%coord[0]) #concat the ms sets whose names are contained in mslist

scaleweights() #scale the weights using gaussian -> supply width and the height (suggest normalised) include imagaing???

imagecombo()

fitscube()

#You should have a nice fitscube for your data set at various angular resolutions.
# Could extend for multiple coords!?
