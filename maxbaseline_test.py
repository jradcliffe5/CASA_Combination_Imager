try:
    import casac
except ImportError, e:
    print "failed to load casa:\n", e
    exit()
import numpy as np

msName = '1252+5634.ms' #our msname!

tb.open(msName + '/ANTENNA')

maxbaseline = 0
antab = np.ndarray.transpose(tb.getcol('POSITION'))
print antab
for row in antab :
    for row2 in antab:
        xsep = row[0] - row2[0]
        ysep = row[1] - row2[1]
        zsep = row[2] - row2[2]
        hypxy =  np.sqrt((xsep * xsep) + (ysep * ysep))
        hypxyz = np.sqrt((zsep * zsep) + (hypxy * hypxy))
        if hypxyz > maxbaseline :
            print maxbaseline
            maxbaseline = hypxyz
print maxbaseline