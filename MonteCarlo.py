import numpy as np
import pandas as pd
from Orbit import PSCrossing
from TailTrack import TailTracking

class Run(object):

	"""A Series of Orbits

	Arguments:

	numorbits: number of orbits to MC

	Optional Arguments:

	orbitlimsx: (typeofdistribution, minimum x, maximum x) - limits of the orbits - types = ('uniform', minimum, maximum) OR ('normal', mean, sigma)
	orbitlimsy: (typeofdistribution, minimum y, maximum y) - limits of the orbits - types = ('uniform', minimum, maximum) OR ('normal', mean, sigma)
	neutrallinelimsx: (minimum x, maximum x) - limits of the neutral line generation
	neutrallinelimsy: (minimum y, maximum y) - limits of the neutral line generation
	reconprob: the Probability of reconnection occuring during a passage

	Functions:

	details: returns the number of orbits
	locations: returns the locations of the orbits (X,Y) as an array of tuples
	orbits: goes down a level to a list of the individual orbits, which can then be referenced
	allfluxropenumbers: returns the total number of neutral lines created in the run
	allfluxropelocations: returns the location of the centers of the generated neutral lines
	fluxropeobjects: returns all neutral line objects in a list -> each orbit is a separate sublist
	fluxropedataframe: returns a dataframe containing all the neutral line information (will take longer to generate than the objects)
	orbitsdataframe: returns a dataframe containing the information about the orbits (takes a long time to iterate through all orbit objects)

	Not implemented:

	"""

	def __init__(self, numorbits, orbitlimsx = ('uniform', -1.5, -3), orbitlimsy = ('uniform', -2, 2), neutrallinelimsx = ('uniform', -1.5, -3), neutrallinelimsy = ('uniform',-2, 2), reconprob = 0.5, width = (1,5), binwidth = 0.25):

		self.numorbits = numorbits

		self.binwidth = binwidth

		self.orbits = [PSCrossing(n, orbitlimsx, orbitlimsy, neutrallinelimsx, neutrallinelimsy, reconprob, width) for n in range(self.numorbits)]

		self.Grid = TailTracking(tailxlims = [-5., 0.], tailylims = [-2., 2.], dely = float(self.binwidth), delx = float(self.binwidth))


	def details(self):

		line0 = 'Number of Orbits: {}'.format(self.numorbits)
		line1 = 'Number of Flux Ropes: {}'.format(self.allfluxropenumbers())

		return '\n'.join([line0, line1])

	def locations(self):

		Locs = [self.orbits[n].location() for n in range(self.numorbits)]

		return np.asarray(Locs)

	def allfluxropenumbers(self):

		FRopeNums = [self.orbits[n].fluxropenumbers() for n in range(self.numorbits)]

		return np.sum(FRopeNums)

	def allfluxropelocations(self):

		FRopeLocs = [self.orbits[n].fluxropelocations() for n in range(self.numorbits)]

		return np.asarray(FRopeLocs)

	def fluxropeobjects(self):

		FRopes = [self.orbits[n].FluxRopes for n in range(self.numorbits) if len(self.orbits[n].FluxRopes) >= 1]

		return FRopes

	def CreateOrbitGrid(self):

		for n in range(self.numorbits):

			for m in range(self.orbits[n].fluxropenumbers()):

				self.Grid.AddFluxRope([self.orbits[n].FluxRopes[m].location()[0],self.orbits[n].FluxRopes[m].location()[1]], self.orbits[n].FluxRopes[m].width)

		return self.Grid.ReturnGrid()

	def fluxropedataframe(self):

		columns = ['OrbitNumber', 'SpacecraftLocationX', 'SpacecraftLocationY', 'ReconnectionLocationX', 'ReconnectionLocationY', 'ReconnectionWidth', 'OverSC', 'Direction']
		index = np.arange(self.allfluxropenumbers())

		df = pd.DataFrame(index = index, columns = columns)

		Counter = 0
		for n in range(self.numorbits):

			for m in range(self.orbits[n].fluxropenumbers()):

				df.loc[Counter] = [n, self.orbits[n].location()[0], self.orbits[n].location()[1], self.orbits[n].FluxRopes[m].location()[0],self.orbits[n].FluxRopes[m].location()[1], self.orbits[n].FluxRopes[m].width, self.orbits[n].FluxRopes[m].det, self.orbits[n].FluxRopes[m].port]

				Counter += 1

		return df

	def orbitsdataframe(self):

		columns = ['OrbitNumber', 'SpacecraftLocationX', 'SpacecraftLocationY', 'NumberOfFluxRopes', 'Duration']
		index = np.arange(self.numorbits)

		df = pd.DataFrame(index = index, columns = columns)

		Counter = 0
		for n in range(self.numorbits):

			df.loc[Counter] = [n, self.orbits[n].location()[0], self.orbits[n].location()[1], len(self.orbits[n].FluxRopes), self.orbits[n].duration]

			Counter += 1

		return df
