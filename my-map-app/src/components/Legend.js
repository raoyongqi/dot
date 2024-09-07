import React from 'react';

const Legend = () => {
  const legendItems = [
    { color: 'green', label: 'Low PL' },
    { color: 'yellow', label: 'Medium PL' },
    { color: 'orange', label: 'High PL' },
    { color: 'red', label: 'Very High PL' }
  ];

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
        {legendItems.map((item, index) => (
          <li key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
            <div style={{
              width: '20px',
              height: '20px',
              backgroundColor: item.color,
              marginRight: '10px',
              border: '1px solid #ddd'
            }}></div>
            {item.label}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Legend;
