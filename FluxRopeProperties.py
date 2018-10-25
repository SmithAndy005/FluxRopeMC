import numpy as np
import pandas as pd
from FluxRopeModeling import FluxRopeProperties

#### Option to import current sheet properties
# CSEncounter = pd.read_csv(r'CS_Stats.csv', index_col = 0, parse_dates = True)

class FluxRopeMC(object):

	"""A Flux Rope MC generator

	Arguments:

		NumberToGenerate:  the number of flux ropes to generate
		IPLims: Limits of the uniform distribution from which to draw IPs
		B0Lims: Limits of the uniform distribution from which to draw B0s
		VxLims: Limits of the uniform distribution from which to draw Vxs
		R0Lims: Limits of the uniform distribution from which to draw R0s

	Functions:

		details: returns a string with basic information
		DF: returns a dataframe of the flux ropes

	Not implemented:



	"""

	def __init__(self, NumberToGenerate, B0Lims = (5., 50.), IPLims = (0., 0.99), VxLims = (250., 1000.), R0Lims = (50., 1000.)):

		self.number = NumberToGenerate
		self.IPLims = IPLims
		self.B0Lims = B0Lims
		self.VxLims = VxLims
		self.R0Lims = R0Lims

		self.FluxRopes = [FluxRopeGenerator(self.IPLims, self.B0Lims, self.VxLims, self.R0Lims) for n in range(NumberToGenerate)]

	def details(self):

		line0 = 'Number of Flux Ropes: {}'.format(self.number)

		return line0

	def DF(self):

		columns = ['ImpactParameter', 'CoreField', 'Velocity', 'Radius', 'DeltaBz', 'Duration', 'StDevBz', 'AvBy', 'AvBtot', 'ByMax', 'BtotMax']
		index = [0]

		df = pd.DataFrame(index = index, columns = columns)

		for n in range(self.number):

			df.loc[n] = [self.FluxRopes[n].IP, self.FluxRopes[n].B0, self.FluxRopes[n].Vx, self.FluxRopes[n].R0, self.FluxRopes[n].DeltaBz, self.FluxRopes[n].Duration, self.FluxRopes[n].stdevbz, self.FluxRopes[n].AvBy, self.FluxRopes[n].AvBtot, self.FluxRopes[n].ByMax, self.FluxRopes[n].BtotMax]

		return df


class FluxRopeGenerator(object):

	"""A Flux Rope object

	Arguments:

		IPLims: Limits of the uniform distribution from which to draw IPs
		B0Lims: Limits of the uniform distribution from which to draw B0s
		VxLims: Limits of the uniform distribution from which to draw Vxs
		R0Lims: Limits of the uniform distribution from which to draw R0s

	Functions:

		B0: Core field between (B0Low, B0High)
		IP: Impact Parameter between (IPLow, IPHigh)
		Vx: Velocity over the spacecraft between (VxLow, VxHigh)
		R0: Radius of the flux rope between (R0Low, R0High)

		DeltaBz: Magnitude of the magnetic deflection in nT
		Duration: Duration of the signature in s
		ByMax: Peak Axial field in nT
		BtotMax = Peak Total Field in nT


	Not implemented:

	"""


	def __init__(self, IPLims, B0Lims, VxLims, R0Lims):

		self.IP = np.random.uniform(IPLims[0], IPLims[1])
		self.B0 = np.random.uniform(B0Lims[0], B0Lims[1])
		self.Vx = np.random.uniform(VxLims[0], VxLims[1])
		self.R0 = np.random.uniform(R0Lims[0], R0Lims[1])

		self.props = FluxRopeProperties(self.IP, self.B0, self.Vx, self.R0)
		self.DeltaBz = self.props[0]
		self.Duration = self.props[1]
		self.ByMax = self.props[2]
		self.BtotMax = self.props[3]


		#### Selecting a random current sheet crossing and properties
		# randindex = np.random.choice(CSEncounter.index)
		# self.stdevbz = CSEncounter.ix[randindex].PSSTDevBz
		# self.AvBy = CSEncounter.ix[randindex].PSAvBy
		# self.AvBtot = CSEncounter.ix[randindex].PSAvBtot

		#### Using dummy values
		self.stdevbz = np.random.normal(0, 20)
		self.AvBy = np.random.normal(0, 20)
		self.AvBtot = np.random.uniform(10, 80)











