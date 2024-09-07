import React, { useEffect } from 'react';
import { capitals } from './site.js'; // 导入 capitals 数据

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
      const circleMarker = new window.AMap.CircleMarker({
        center: center,
        radius: 2 + Math.random() * 2,
        strokeColor: 'white',
        strokeWeight: 2,
        strokeOpacity: 0.5,
        fillColor: 'rgba(0,0,255,1)',
        fillOpacity: 0.5,
        zIndex: 10,
        bubble: true,
        cursor: 'pointer',
        clickable: true
      });
      circleMarker.setMap(map);
    });
  }, []);

  return <div id="map" style={{ width: '100%', height: '100%' }}></div>;
};

export default MapComponent;
