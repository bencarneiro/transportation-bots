import logo from './logo.svg';
import './App.css';
import TimeSeriesChart from  './TimeSeries.js'

import axios from "axios"
import React, { useState } from 'react';

function App() {

  React.useEffect(() => {
    axios.get('http://localhost:8000/get_expense_timeseries/?transit_agency_id=1&uza=14')
        .then(response => setData(response.data.data));
  }, []);
  const [data, setData] = React.useState(null)

  
        
  console.log(data)
  return (
    <div className="App">
     
      <body><TimeSeriesChart chartData={data}/></body>
    </div>
  );
}

export default App;
