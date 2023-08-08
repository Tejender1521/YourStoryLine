import * as React from "react";
import Map, { Marker } from "react-map-gl";
import "./map.css";
import { motion } from "framer-motion";
import mapboxgl from "mapbox-gl/dist/mapbox-gl";

import "mapbox-gl/dist/mapbox-gl.css";

// eslint-disable-next-line import/no-webpack-loader-syntax
// import MapboxWorker from "worker-loader!mapbox-gl/dist/mapbox-gl-csp-worker";

// eslint-disable-next-line import/no-webpack-loader-syntax
mapboxgl.workerClass = require('worker-loader!mapbox-gl/dist/mapbox-gl-csp-worker').default;

export default function Mapbox(props) {
  const data = props?.data;

  
  return (
    <Map
      mapboxAccessToken={process.env.REACT_APP_MAP_KEY}
      initialViewState={{
        longitude: 75.6340804153019,
        latitude: 26.91026351703445,
        zoom: 10,
      }}
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
      }}
      mapStyle="mapbox://styles/mapbox/streets-v9"
    >
      {data &&
        Object.keys(data)?.map((item, index) => {
          const lat = data[item].place_data.geometry.coordinates[1];
          const lon = data[item].place_data.geometry.coordinates[0];

          return (
            <Marker
              key={index}
              latitude={lat || 26.91026351703445}
              longitude={lon || 75.6340804153019}
            >
              <motion.img
                whileHover={{ scale: 1.4 }}
                whileTap={{ scale: 0.9 }}
                src={require("../../assests/mappin1.png")}
                alt=""
                className="tooltip"
              />
            </Marker>
          );
        })}
    </Map>
  );
}
