
def FluxRopeProperties(IP, B0, Vx, R):

	import numpy as np
	from scipy import special

	ImpactParameter = IP
	CoreField = B0
	R0 = 1.
	Radius = float(R) # In km
	Velocity = float(Vx) # In kms-1

	alpha_max = 2 * np.arccos(float(ImpactParameter))
	a_max = 2 * np.sin(alpha_max/2.) #This is the length of the Chord in units of radius


	DistanceTraversedInFrope = Radius*a_max

	DurationOfSignature = DistanceTraversedInFrope/Velocity


	#### First Point
	DistanceFromClosestApproachFirst = -(a_max / 2)
	#### Last Point
	DistanceFromClosestApproachLast = (a_max / 2)

	if ImpactParameter == 0.:
		ThetaFirst = 0.
		ThetaLast = 0.
	else:
		ThetaFirst = np.arctan(DistanceFromClosestApproachFirst/ImpactParameter)
		ThetaLast = np.arctan(DistanceFromClosestApproachLast/ImpactParameter)


	phiFirst = np.pi/2. - abs(ThetaFirst)
	phiLast = np.pi/2. - abs(ThetaLast)

	r = 1.

	Baxial = B0 * special.jv(0, r * (2.4048/R0)) # Can really ignore this if we're only interested in |Delta Bz|
	Bazimuth = B0 * special.jv(1, r * (2.4048/R0)) #Removed Helicity as just interested in the |Delta Bz|

	if ImpactParameter == 0.:
		BzFirst = -Bazimuth
		BzLast = Bazimuth

		DeltaBz = BzLast - BzFirst


	else:
		BzFirst = Bazimuth * np.sin(ThetaFirst)
		BzLast = Bazimuth * np.sin(ThetaLast)

		DeltaBz = BzLast - BzFirst


	ByMax = B0 * special.jv(0, ImpactParameter * (2.4048/R0))
	BazMiddle = B0 * special.jv(1, ImpactParameter * (2.4048/R0))
	BtotMax = (ByMax**2 + BazMiddle**2)**0.5

	return [DeltaBz, DurationOfSignature, ByMax, BtotMax]



