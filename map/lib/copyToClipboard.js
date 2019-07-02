function execCopy(string){
	// Create an empty tag.
	var tmp = document.createElement("div");
	var dummy = document.createElement('p');

	// Configure user selection mode.
	dummy.style.webkitUserSelect = 'auto';
	dummy.style.userSelect = 'auto';

	tmp.appendChild(dummy).textContent = string;

	// Put the dummy tag outside of the window not to see the dummy.
	var style = tmp.style;
	style.position = 'fixed';
	style.right = '200%';

	// Add dummy entity to body.
	document.body.appendChild(tmp);
	document.getSelection().selectAllChildren(tmp);

	// Copy to clipboard.
	var result = document.execCommand("copy");

	// Remove temporal tag.
	document.body.removeChild(tmp);

	return result;
}

var popup = L.popup();

function copyCoord(e) {
	var original = e.latlng.toString();
	
	const pickUrl = (str) => str.substring(str.indexOf('LatLng(') + 7, str.length - 1);
	var extracted = pickUrl(original).split(", ");
	
	if(execCopy(extracted)){
		popup.setLatLng(e.latlng).setContent(extracted).openOn(mymap);
	} else {
		execCopy("false");
		return(false);
	}
}


