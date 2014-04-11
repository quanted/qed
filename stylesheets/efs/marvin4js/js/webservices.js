// Define the default location of webservices

function getDefaultServicesPrefix() {
	var servername = "";
//	var webapp = "http://localhost:8111/webservices";
	var webapp = "http://pnnl.cloudapp.net/webservices";
	return servername + webapp;
}

function getDefaultServices() {
	var base = getDefaultServicesPrefix();
	var services = {
			"clean2dws" : base + "/rest-v0/util/convert/clean",
			"molconvertws" : base + "/rest-v0/util/calculate/molExport",
			"stereoinfows" : base + "/rest-v0/util/calculate/cipStereoInfo",
			"molDetails" : base + "/rest-v0/util/detail"
	};
	return services;
}
