import logo from './logo.svg';
import './App.css';
import TimeSeriesChart from  './TimeSeries.js'
import BarChart from './BarChart.js'

import axios from "axios"
import React, { useState } from 'react';

function App() {

  React.useEffect(() => {
    axios.get('http://localhost:8000/upt_by_mode_type/?ntd_id=1')
        .then(response => setData(response.data.data));
  }, []);
  const [data, setData] = React.useState(null)

  
        
  console.log(data)
  return (
    <div className="App">
     
      <body>
        <></>
        <BarChart chartData={data}/>
        <h2>Test Title</h2>
        {/* <TimeSeriesChart chartData={data}/> */}
      </body>
    </div>
  );
}

export default App;
