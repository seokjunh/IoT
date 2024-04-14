import React, { useState, useEffect } from 'react';

const Streaming = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const socket = new WebSocket('ws://192.168.0.220:8001/ws');
    socket.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setData(newData);
    };

    return () => {
      socket.close();
    };
  }, []);

  const getQuadrantColor = (quadrant) => {
    const value = data[quadrant];
    if (value && value > 80) {
      return 'bg-red-500';
    }
    if (value && value > 40) {
      return 'bg-orange-500';
    }
    if (value && value > 20) {
      return 'bg-yellow-500';
    }
    return 'bg-opacity-0';
  };

  return (
    <div className="relative h-screen">
      <img
        src="http://192.168.0.220:8000/video_feed"
        className="w-full h-full object-cover"
      />
      <div
        className={`absolute top-0 left-0 w-1/2 h-1/2 opacity-50 ${getQuadrantColor(
          'A0'
        )}`}
      ></div>
      <div
        className={`absolute top-0 right-0 w-1/2 h-1/2 opacity-50 ${getQuadrantColor(
          'A1'
        )}`}
      ></div>
      <div
        className={`absolute bottom-0 left-0 w-1/2 h-1/2 opacity-50 ${getQuadrantColor(
          'A2'
        )}`}
      ></div>
      <div
        className={`absolute bottom-0 right-0 w-1/2 h-1/2 opacity-50 ${getQuadrantColor(
          'A3'
        )}`}
      ></div>
      <div className="absolute top-0 left-1/2 w-0.5 h-full bg-white"></div>
      <div className="absolute top-1/2 left-0 w-full h-0.5 bg-white"></div>
      <div className="absolute top-0 right-1/2 w-0.5 h-full bg-white"></div>
      <div className="absolute bottom-0 left-0 w-full h-0.5 bg-white"></div>
    </div>
  );
};

export default Streaming;
