##############Packages##############################################################################################################
import numpy as np
from scipy.special import erf
from scipy.constants import c as clight
from matplotlib import pyplot as plt
import os

##########Import casa packages######################################################################################################
try:
    import casac
except ImportError, e:
    print "failed to load casa:\n", e
    exit()

plt.rcParams['axes.formatter.limits'] = [-4,4]
plt.close()

def round2n(x, base):
    return int(base * round(float(x)/base))
#############################################
######Define max baseline####################
#############################################
def maxbaseline(msName):
    maxbaseline = 0
    tb.open(msName + '/ANTENNA')
    antab = np.ndarray.transpose(tb.getcol('POSITION'))
    antab=antab[~np.all(antab == 0, axis=1)] #removes any zero rows..eMERLIN!
    tb.close()
    for row in antab :
        for row2 in antab:
            xsep = row[0] - row2[0]
            ysep = row[1] - row2[1]
            zsep = row[2] - row2[2]
            hypxy =  np.sqrt((xsep * xsep) + (ysep * ysep))
            hypxyz = np.sqrt((zsep * zsep) + (hypxy * hypxy))
            if hypxyz > maxbaseline :
                maxbaseline = hypxyz
    return maxbaseline

##############################################
##############Inputs##########################
##############################################
#msName = '1252+5634.ms'
#msName ='HDFC0155MFSC_CAL_vis.ms'
msName = 'SN2014C_L_AVGFITS_20150503.DQUAL.1.ms'
imagesize = 540 #in arcsecs
##############################################
#######Parse the info from .ms################
##############################################

## Open the table to get individual weightings
tb.open(msName)


# Read the UVWs and weighting from the table
UVW = tb.getcol('UVW').T
print UVW[1]
weights = tb.getcol('WEIGHT')
print np.shape(weights)


# Close the table
tb.close()
tb.open(msName + '/SPECTRAL_WINDOW')
refFreq = tb.getcol('REF_FREQUENCY')
nChan = tb.getcol('NUM_CHAN')
totBW = tb.getcol('TOTAL_BANDWIDTH')

widthChan = totBW/nChan
cfreq = refFreq[0]+ np.sum(totBW)/2.
# Read the REF_FREQUENCY and NUM_CHAN and TOTAL_BANDWIDTH into np arrays
tb.close()
#find the UV distance using a bit of trigonomtry
#uvdist = []
uvdist = np.sqrt((UVW[:,0] * UVW[:,0]) + (UVW[:,1] * UVW[:,1]))

#stack these w.r.t to weights which have four entries for each pol
uvdist = np.vstack((uvdist,weights))
print uvdist
#Add index so we can remember the original order when we resort
index = np.linspace(0,int(uvdist.shape[1]-1),int(uvdist.shape[1]))
uvdist = np.vstack((uvdist,index))

#and find the beam size maximum
HPBW = 1.22*(clight/((cfreq)*maxbaseline(msName)))*(180./np.pi)*3600. ##needs to be checked!!
sampling = HPBW/3.
imagesize_im = int(round2n(imagesize/sampling,128))
imagesize_im = [imagesize_im,imagesize_im]
if imagesize_im == [0,0]:
    imagesize_im = [128,128]
print imagesize_im
#Order the table in place by the first column ascending
order = uvdist[0,:].argsort()
uvdist = np.take(uvdist, order, 1)

#Plot our original weights w.r.t to UV distance
plt.figure(1)
plt.plot(uvdist[0,:],uvdist[1,:],'.')
plt.xlabel('UV distance ($\lambda$)')
plt.ylabel('Weight')
plt.show()


uvinterval = np.linspace(0,np.amax(uvdist[0,:]),10) #get central points for the Gaussian weighting fcn!
for i in range(len(uvinterval)):
    #######################################
    #######Create gaussian function########
    #######################################
    # Create a gaussian with normalised amplitude and width sigma!

    sigma = 80000
    gaussweight = np.exp((-1*np.square(uvdist[0,:]-uvinterval[i])/(2*np.square(sigma))))
    gaussweight[gaussweight >= 1E308] = 0
    
    #Make plot of the gaussian weighting functions used in the imaging
    plt.figure(2)
    plt.plot(uvdist[0,:],gaussweight,'.',label=str(np.round(uvinterval[i],decimals=0))+' $\lambda$')
    plt.xlabel('UV distance ($\lambda$)')
    plt.ylabel('Weight')
    plt.legend()
    plt.show()
    
    uvdist_mod=[]
    #Make new uvdist with the modified gaussian weighting attached
    uvdist_mod = np.vstack((uvdist,gaussweight))
    #Resort in original visibility order
    order = uvdist_mod[int(np.shape(weights)[0]+1),:].argsort()
    uvdist_mod = np.take(uvdist_mod, order, 1)
    
    #Combine number of N_pol times to account for pol products in the casa table
    gaussweight = np.array([uvdist_mod[int(np.shape(weights)[0]+2),:],]*np.shape(weights)[0])
    
    #Overwrite the weight table in Casa with the gaussian weighting
    tb.open(msName,nomodify=False)
    data=tb.getcol("WEIGHT")
    tb.putcol("WEIGHT", gaussweight)
    tb.flush()
    tb.close()
    
    #Produce the image + export a fits file
    clean(vis=msName,imagename=msName[:-3]+'_'+str(i),mode='mfs',gridmode='widefield',wprojplanes=-1,niter=10000,imsize=imagesize_im,cell=str(sampling)+'arcsec',weighting='natural')
    exportfits(imagename=msName[:-3]+'_'+str(i)+'.image', fitsimage=msName[:-3]+'_'+str(i)+'.fits', history=False)
'''
#Overwrite the weight table in Casa with the original weighting from the calibration.
tb.open(msName,nomodify=False)
data=tb.getcol("WEIGHT")
tb.putcol("WEIGHT", weights)
tb.flush()
tb.close()
'''