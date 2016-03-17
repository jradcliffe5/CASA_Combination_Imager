try:
    import casac,os
except ImportError, e:
    print "failed to load casa:\n", e
    exit(1)
mstool = casac.homefinder.find_home_by_name('msHome')
ms = casac.ms = mstool.create()
tbtool = casac.homefinder.find_home_by_name('tableHome')
tb = casac.tb = tbtool.create()


