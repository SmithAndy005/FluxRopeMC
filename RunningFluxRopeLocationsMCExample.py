
from MonteCarlo import Run

print 'Number of Orbits Required: ' 
R = int(raw_input())
print 'Running MC'
X = Run(10, orbitlimsx = ('uniform', -1.5, -3.), orbitlimsy = ('uniform', -2., 2.), width = (1, 4), reconprob = 0.5)
print 'Formatting Data'

Grid = X.CreateOrbitGrid()
OrbitDF = X.orbitsdataframe()
FluxRopes = X.fluxropedataframe()

print FluxRopes


