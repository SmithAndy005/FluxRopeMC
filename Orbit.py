from FluxRope import FluxRope
import numpy as np
import pandas as pd

class PSCrossing(object):

	"""The individual crossing of the plasma sheet.

	Arguments:
		index:  a numerical value to refer to the crossing
		(typeofdistribution, locxlow, locxhigh): limits for location in x direction - types = ('uniform', minimum, maximum) OR ('normal', mean, sigma)
		(typeofdistribution, locylow, locyhigh): limits for location in y direction - types = ('uniform', minimum, maximum) OR ('normal', mean, sigma)
		(neutrallinelimxmin, neutrallinelimxmax): limits for neutral line in x direction
		(neutrallinelimymin, neutrallinelimymax): limits for neutral line in y direction
		reconprob: probability of a neutral line being generated during passage
		(widthmin, widthmax): limits for width of neutral line in units of R_M

	Functions:

		index: returns the index
		duration: returns a randomly selected duration from Poh et al., 2016 catalogue.
		details: returns the index, location
		location: returns a tuple (X, Y)
		FluxRopes: returns the instance of the flux ropes
		fluxropelocations: returns an array of tuples corresponding to the location of flux ropes
		fluxropenumbers: returns the number of flux ropes in the orbit

	Not implemented:

		lobefieldstrength: the lobe field preceeding
		plasmasheetsigmabz: the variation in the field within the plasma sheet

	"""

	def __init__(self, index, orbitlimsx, orbitlimsy, (disttypex, neutrallinelimxmin, neutrallinelimxmax), (disttypey, neutrallinelimymin, neutrallinelimymax), reconprob, (widthmin, widthmax)):

		"""Creates the PSCrossing object
		"""

		self.index = index

		#### Option to put in real orbits
		# CSEncounter = pd.read_csv(r'CrossingList.csv', index_col = 0, parse_dates = True)

		self.locxtype = orbitlimsx[0]
		self.locytype = orbitlimsy[0]

		#### Inputting the real orbits if required
		# if self.locxtype == 'messenger_o':
		# 	self.duration = CSEncounter.Duration.values[self.index % (len(CSEncounter.index)-1)]
		# else:
		# 	self.duration = np.random.choice(CSEncounter.Duration.values)

		self.duration = np.random.uniform(0, 10)

		"""Generating Parameters:

		locx: spacecraft location in x
		locy: spacecraft location in y

		"""

		if self.locxtype == 'uniform':
			self.locx = np.random.uniform(orbitlimsx[1], orbitlimsx[2])
		elif self.locxtype == 'normal':
			self.locx = np.random.normal(orbitlimsx[1], orbitlimsx[2])
		# elif self.locxtype == 'messenger_r':
		# 	JumbledCS = CSEncounter.sample(frac=1)
		# 	self.locx = JumbledCS['X_MSM_Ab'].values[0]
		# elif self.locxtype == 'messenger_o':
		# 	self.locx = CSEncounter['X_MSM_Ab'].values[self.index % (len(CSEncounter.index)-1)]

		if self.locytype == 'uniform':
			self.locy = np.random.uniform(orbitlimsy[1], orbitlimsy[2])
		elif self.locytype == 'normal':
			self.locy = np.random.normal(orbitlimsy[1], orbitlimsy[2])
		# elif self.locytype == 'messenger_r':
		# 	JumbledCS = CSEncounter.sample(frac=1)
		# 	self.locy = JumbledCS['Y_MSM_Ab'].values[0]
		# elif self.locytype == 'messenger_o':
			# self.locy = CSEncounter['Y_MSM_Ab'].values[self.index % (len(CSEncounter.index)-1)]

		MCNumber = np.random.random(1)

		if MCNumber <= reconprob: # Probability of a reconnection instance occuring
			NumberOfFluxRopes = 1
			self.FluxRopes = [FluxRope(n, (disttypex, neutrallinelimxmin, neutrallinelimxmax), (disttypey, neutrallinelimymin, neutrallinelimymax), (widthmin, widthmax), (self.locx, self.locy)) for n in range(NumberOfFluxRopes)]
		else:
			self.FluxRopes = []

	def details(self):

		line0 = 'Index: {}'.format(self.index)
		line1 = 'S/C Location (X Y): ({}, {})'.format(self.locx, self.locy)

		return '\n'.join([line0, line1])

	def location(self):
		return (self.locx, self.locy)

	def fluxropelocations(self):
		if len(self.FluxRopes) == 0:
			return np.asarray([])
		else:
			FRopeLocs = [F.location() for F in self.FluxRopes]
			return np.asarray(FRopeLocs)

	def fluxropenumbers(self):
		return len(self.FluxRopes)
