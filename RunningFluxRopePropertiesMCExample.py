from FluxRopeProperties import FluxRopeMC

print 'Number of Flux Ropes Required: ' 
R = int(raw_input())
print 'Running MC'
X = FluxRopeMC(R, B0Lims = (50., 68.), IPLims = (0., 0.99), VxLims = (250., 1500.), R0Lims = (25., 800.))
print 'Formatting Data'
FRopeDataFrame = X.DF()

print FRopeDataFrame
