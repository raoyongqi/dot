import React from 'react';
import { capitals } from '../data/site.js'; // Import capitals data to get the color ranges

const Legend = () => {
  // Get unique color and PL range pairs
  const uniqueColorRanges = [...new Set(capitals.map(capital => JSON.stringify(capital.color)))].map(item => JSON.parse(item));

  return (
    <div style={{
      position: 'absolute',
      top: 10,
      right: 10,
      backgroundColor: 'white',
      padding: '10px',
      border: '1px solid #ccc',
      borderRadius: '4px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
      zIndex: 1000
    }}>
      <h4>Legend</h4>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {uniqueColorRanges.map((colorRange, index) => (
          <li key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
            <div style={{
              width: '20px',
              height: '20px',
              backgroundColor: colorRange[0], // Use the color value
              marginRight: '10px',
              border: '1px solid #ddd'
            }}></div>
            <span>{`PL: [${colorRange[1][0].toFixed(2)}, ${colorRange[1][1].toFixed(2)}]`}</span> {/* Display the PL range */}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Legend;
