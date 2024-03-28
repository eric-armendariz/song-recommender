import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/playlists").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>
      {(typeof data['items'] === 'undefined') ? (
        <p>Loading...</p>
      ) : (
        <div className='image-container'>
          {data['items'].map((item, i) => {

            if (item && Object.keys(item).includes('images') && item['images']
              && Object.keys(item['images'][0]).includes('url')) {
                const imageUrl = item['images'][0]['url'];  // Declare imageUrl using const
                console.log(Object.keys(item['images'][0]['url']))
        
                return (
                  <div className='image-item' key={i}>
                    <div className='image-wrapper'>
                      <img src={imageUrl}/>
                      <p className='image-text'>{item['name']}</p>
                    </div>
                  </div>
                );
            }
            return null;
          })}
        </div>  
        )}
    </div>
  );
}

export default App