import numpy as np

class FluxRope(object):

	"""A Flux Rope object with defined location, size, etc.

	Arguments:

		index:  a numerical value to refer to the crossing
		(typeofdistribution, locxlow, locxhigh): limits for location in x direction - types = ('uniform', minimum, maximum) OR ('normal', mean, sigma)
		(typeofdistribution, locylow, locyhigh): limits for location in y direction - types = ('uniform', minimum, maximum) OR ('normal', mean, sigma)
		(minwidth, maxwidth): minimum and maximum width of the flux rope
		(scx, scy): location of the spacecraft

	Functions:

		index: returns the numerical index for the flux rope
		details(): returns information about the flux rope
		locx: xlocation of the reconnection site
		locy: ylocation of the reconnection site
		location(): returns a tuple (X, Y) for the location of the flux rope
		width: the cross tail extent of the flux rope
		det: whether it would pass over the spacecraft (0, 1): (No, Yes)
		port: planetward or tailward travelling product at sc location (p, t)

	Not implemented:

		radius: the radius of the flux rope
		velocity: the velocity of the flux rope
		core field: the strength of the core field of the flux rope

	"""

	def __init__(self, index, (xtype, locxlow, locxhigh), (ytype, locylow, locyhigh), (minwidth, maxwidth), (scx, scy)):

		self.index = index

		"""Generating Parameters:

		locx: between the limits (locxlow and locxhigh) from a given distribution
		locy: between the limits (locylow and locyhigh) from a given distribution
		width: between the limits (minwidth and maxwidth) from a uniform distribution
		port: whether the spacecraft will detect a tailward or planetward moving flux rope
		det: whether the flux rope passes over the spacecraft

		maxy: maximum yvalue the flux rope reaches
		miny: mimumum yvalues the flux rope reaches

		"""

		self.locxtype = xtype
		self.locytype = ytype

		if self.locxtype == 'uniform':
			self.locx = np.random.uniform(locxlow, locxhigh)
		elif self.locxtype == 'normal':
			self.locx = np.random.normal(locxlow, locxhigh)
			if self.locx > 0:
				while self.locx > 0:
					self.locx = np.random.normal(locxlow, locxhigh)

		if self.locytype == 'uniform':
			self.locy = np.random.uniform(locylow, locyhigh)
		elif self.locytype == 'normal':
			self.locy = np.random.normal(locylow, locyhigh)
			if (self.locy < -2) or (self.locy > 2):
				while (self.locy < -2) or (self.locy > 2):
					self.locy = np.random.normal(locylow, locyhigh)

		self.width = np.random.uniform(minwidth, maxwidth)

		self.maxy = self.locy + self.width/2.
		self.miny = self.locy - self.width/2.

		if self.locx < scx:
			self.port = 'p'
		else:
			self.port = 't'

		if (self.maxy > scy) and (self.miny < scy):
			self.det = 1
		else:
			self.det = 0

	def details(self):

		line0 = 'Flux Rope Index: {}'.format(self.index)
		line1 = 'Flux Rope Origin Location (X, Y): ({}, {})'.format(self.locx, self.locy)
		line2 = 'Flux Rope Width: {}'.format(self.width)
		line3 = 'Flux Rope Ends (MaxY, MinY): ({}, {})'.format(self.maxy, self.miny)
		line4 = 'Flux Rope Detected?: {}'.format(self.det)
		line5 = 'Planetward or Tailward Moving (p/t): {}'.format(self.port)

		return '\n'.join([line0, line1, line2, line3, line4, line5])

	def location(self):
		return (self.locx, self.locy)
