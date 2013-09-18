class geneec(object):
	def __init__(self, chem_name, application_target, application_rate, number_of_applications, interval_between_applications, Koc, aerobic_soil_metabolism, wet_in, application_method, application_method_label, aerial_size_dist, ground_spray_type, airblast_type, spray_quality, no_spray_drift, incorporation_depth, solubility, aerobic_aquatic_metabolism, hydrolysis, photolysis_aquatic_half_life):
		self.chem_name = chem_name
		self.application_target = application_target
		self.application_rate = application_rate
		self.number_of_applications = number_of_applications
		self.interval_between_applications = interval_between_applications
		self.Koc = Koc
		self.aerobic_soil_metabolism = aerobic_soil_metabolism
		self.wet_in = wet_in
		self.application_method = application_method
		if application_method == 'a':
			self.application_method_label = 'Aerial Spray'
		if application_method == 'b':
			self.application_method_label = 'Ground Spray'
		if application_method == 'c':
			self.application_method_label = 'Airblast Spray (Orchard & Vineyard)'
		if application_method == 'd':
			self.application_method_label = 'Granular (Non-spray)'

		self.aerial_size_dist = aerial_size_dist
		self.ground_spray_type = ground_spray_type
		self.airblast_type = airblast_type
		self.spray_quality = spray_quality
		self.no_spray_drift = no_spray_drift
		self.incorporation_depth = incorporation_depth
		self.solubility = solubility
		self.aerobic_aquatic_metabolism = aerobic_aquatic_metabolism
		self.hydrolysis = hydrolysis
		self.photolysis_aquatic_half_life = photolysis_aquatic_half_life
