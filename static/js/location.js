const funcionInit = () => {
	if (!"geolocation" in navigator) {
		return alert(
			"Tu navegador no soporta el acceso a la ubicación. Intenta con otro"
		);
	}

	const onUbicacionConcedida = (ubicacion) => {
		console.log("Tengo la ubicación: ", ubicacion);
		const coordenadas = ubicacion.coords;
		getcord(coordenadas);
	};
	const onErrorDeUbicacion = (err) => {
		console.log("Error obteniendo ubicación: ", err);
		alert("No se pudo obtener la ubicación");
	};

	const opcionesDeSolicitud = {
		enableHighAccuracy: true, // Alta precisión
		maximumAge: 0, // No queremos caché
		timeout: 5000, // Esperar solo 5 segundos
	};

	navigator.geolocation.getCurrentPosition(
		onUbicacionConcedida,
		//onErrorDeUbicacion,
		opcionesDeSolicitud
	);
};

funcionInit();
