# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 09:42:16 2015

@author: jackradcliffe
"""
msName = '1252+5634.ms'

try:
    import casac
except ImportError, e:
    print "failed to load casa:\n", e
    exit(1)

#mstool = casac.homefinder.find_home_by_name('msHome')
#ms = casac.ms = mstool.create()
#tbtool = casac.homefinder.find_home_by_name('tableHome')
#tb = casac.tb #= tbtool.create()

# It's a good habit to create a new instance of the tool first, to
# avoid possible collisions:

# You need to define msName='myMS.ms' first -- then, this will 
# open the table with spectral window information
tb.open(msName + '/SPECTRAL_WINDOW')
# Read the REF_FREQUENCY and NUM_CHAN columns into Python arrays
refFreq = tb.getcol('REF_FREQUENCY')
nChan = tb.getcol('NUM_CHAN')
totBW = tb.getcol('TOTAL_BANDWIDTH')
widthChan = totBW/nChan
# Close the table
tb.close()
# The SPW index is simply the row number in SPECTRAL_WINDOW
spwObs = len(refFreq)

print 'The frequency information for BW averaging of data set %s is' % msName
print 'No. Spectral Windows:  %d' % spwObs
print 'Bandwidth per spw:     %f Hz' % totBW[0]
print 'No. Channels per spw:  %d' % nChan[0]
print 'and the channel width: %f Hz' % widthChan[0]