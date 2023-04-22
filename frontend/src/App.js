import logo from './logo.svg';
import './App.css';
import TimeSeriesChart from  './TimeSeries.js'

import axios from "axios"
import React, { useState } from 'react';

function App() {

  React.useEffect(() => {
    axios.get('http://localhost:8000/get_expense_timeseries_group_by_mode/?ntd_id=60048')
        .then(response => setData(response.data.data));
  }, []);
  const [data, setData] = React.useState(null)

  
        
  console.log(data)
  return (
    <div className="App">
     
      <body>
        <></>
        <TimeSeriesChart  title="Chart of PU x UV" chartData={data}/>
        <TimeSeriesChart  title="Chart of PU x UV" chartData={data}/>
        <TimeSeriesChart chartData={data}/>
        <TimeSeriesChart chartData={data}/>
        <TimeSeriesChart chartData={data}/>
        <h2>Test Title</h2>
        <TimeSeriesChart chartData={data}/>
      </body>
    </div>
  );
}

export default App;
