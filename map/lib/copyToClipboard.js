function copyCoord(e) {
	var latlon = e.latlng.toString();
	var lat = latlon.split(",")[0].replace("LatLng(","");
	var lon = latlon.split(",")[1].replace(")","");
	alert(lat + lon);
}

