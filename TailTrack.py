import numpy as np

class TailTracking(object):

	"""Object to keep track of where flux ropes have covered the tail

	Arguments:



	Optional Arguments:

	taillimsx: (minimum x, maximum x)
	taillimsy: (minimum y, maximum y)
	dely: spacing of the bins in y
	delx = spacing of the bins in x

	Functions:

	AddFluxRope(center, width):
		center: center of the flux rope (x, y) - only the y is important currently as assuming pure planetward/tailward flow
		width: width of the flux rope
	ReturnGrid():

	Not implemented:

	"""

	def __init__(self, tailxlims = [-5., 0.], tailylims = [-2., 2.], dely = 0.25, delx = 0.25):

		### Generate2D array of zeros covering the tail
		# self.Grid = np.zeros(tailxlims)
		self.Grid = np.zeros((int((tailxlims[1] - tailxlims[0])/delx), int((tailylims[1] - tailylims[0])/dely)))

		self.tailxlims = tailxlims
		self.tailylims = tailylims
		self.dely = dely
		self.delx = delx


	def AddFluxRope(self, center, width):

		TopEnd = center[1]+width/2
		LowerEnd = center[1]-width/2

		ColHeader = np.arange(self.tailylims[0]+self.dely/2, self.tailylims[1]+self.dely/2, self.dely)

		for n, C in enumerate(ColHeader):

			# print '####', n, C

			if (C+self.dely/2 > TopEnd) and (C-self.dely/2 < TopEnd):

				MaxExtent = C
				MaxExtentIndex = n

			if (C+self.dely/2 > LowerEnd) and (C-self.dely/2 < LowerEnd):

				MinExtent = C
				MinExtentIndex = n

			if C-self.dely/2 == LowerEnd:

				MinExtent = C
				MinExtentIndex = n

			if C+self.dely/2 == TopEnd:

				MaxExtent = C
				MaxExtentIndex = n

		if LowerEnd	< ColHeader[0]-self.dely/2:
			MinExtent = ColHeader[0]
			MinExtentIndex = 0

		if TopEnd > ColHeader[-1]+self.dely/2:
			MaxExtent = ColHeader[-1]
			MaxExtentIndex = -1

		# print MaxExtentIndex, MaxExtent
		# print MinExtentIndex, MinExtent

		### Take a slice and add one

		try:
			if MaxExtentIndex == -1:
				self.Grid[:,MinExtentIndex:] += 1
			else:
				self.Grid[:,MinExtentIndex:MaxExtentIndex+1] += 1
		except UnboundLocalError:
			print 'Generated Outside the Tail'

	def ReturnGrid(self):

		return self.Grid
