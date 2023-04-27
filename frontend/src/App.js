import logo from './logo.svg';
import './App.css';
import TimeSeriesChart from  './TimeSeries.js'
import BarChart from './BarChart.js'

import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';

function App() {

  React.useEffect(() => {
    axios.get('http://localhost:8000/spending_by_budget/?ntd_id=1')
        .then(response => setData(response.data.data));
  }, []);
  const [data, setData] = React.useState(null)

  
        
  return (
    <div className="App">
     
      <body>
        <></>
        <h2>Expense by Budget</h2>
        <SpendingByBudget chartData={data}/>
      </body>
    </div>
  );
}

export default App;
