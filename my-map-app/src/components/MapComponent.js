import React, { useEffect } from 'react';
import { capitals } from '../data/site.js'; // Import capitals data
import Legend from './Legend'; // Import Legend component from the same directory

const MapComponent = () => {
  useEffect(() => {
    // Ensure AMap is loaded
    if (!window.AMap) {
      console.error("AMap is not loaded");
      return;
    }

    const map = new window.AMap.Map('map', {
      zoom: 4,
      center: [108, 34]
    });

    capitals.forEach((capital) => {
      const center = capital.center;
      const color = capital.color; // Use the color from capitals data
      const circleMarker = new window.AMap.CircleMarker({
        center: center,
        radius: 3,
        strokeColor: 'white',
        strokeWeight: 2,
        strokeOpacity: 0.5,
        fillColor: color, // Set fill color based on the data
        fillOpacity: 0.5,
        zIndex: 10,
        bubble: true,
        cursor: 'pointer',
        clickable: true
      });
      circleMarker.setMap(map);
    });
  }, []);

  return (
    <div id="map-container" style={{ position: 'relative', width: '100%', height: '100%' }}>
      <div id="map" style={{ width: '100%', height: '100%' }}></div>
      <Legend />
    </div>
  );
};

export default MapComponent;
