var map = L.map('map').setView([11.01901, -74.85088], 17);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
	attribution:
		'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Declare a global variable to store the routing control
let routingControl;

const createRoutingControl = (start, destination) => {
	return L.Routing.control(
		L.extend(window.lrmConfig, {
			waypoints: [
				L.latLng(start.latitude, start.longitude),
				L.latLng(destination.latitude, destination.longitude),
			],
			router: L.Routing.graphHopper(
				"ef80e7e7-23d7-470c-8cef-c42f10a83d58",
				{
					urlParameters: {
						vehicle: "foot",
					},
				}
			),
			language: "en",
			geocoder: L.Control.Geocoder.nominatim(),
			routeWhileDragging: true,
			reverseWaypoints: true,
			showAlternatives: true,
			eOptions: {
				styles: [
					{ color: "black", opacity: 0.15, weight: 9 },
					{ color: "white", opacity: 0.8, weight: 6 },
					{ color: "blue", opacity: 0.5, weight: 2 },
				],
			},
			RoutingControl: null,
			collapsible: true,
			show: false,
		})
	);
};

const getcord = async (local) => {
	const cord = local;
	var select = document.getElementById("markerPosition");
	var selectedOption = select.options[select.selectedIndex].value.split(', ');
	var destlat = parseFloat(selectedOption[0]);
	var destlng = parseFloat(selectedOption[1]);

	// Remove previous routing control if it exists
	if (routingControl) {
		map.removeControl(routingControl);
	}

	// Create a new routing control
	routingControl = createRoutingControl(cord, { latitude: destlat, longitude: destlng });

	// Add the new routing control to the map

	routingControl.addTo(map);
};
