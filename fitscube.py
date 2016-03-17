from astropy.io import fits

msName = 'HDFC0155MFSC_CAL_vis.ms'
x=fits.getdata(msName[:-3]+'_'+str(0)+'.fits',0)
header_primary = fits.getheader(msName[:-3]+'_'+str(0)+'.fits')
fits.writeto('HDFC0155_cube.fits', x, header_primary)

for i in range(1,8):
    x=fits.getdata(msName[:-3]+'_'+str(i)+'.fits',0)
    header_primary = fits.getheader(msName[:-3]+'_'+str(i)+'.fits')
    fits.append('HDFC0155_cube.fits', x, header_primary)

print fits.info("HDFC0155_cube.fits")