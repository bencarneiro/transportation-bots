import logo from './logo.svg';
import './App.css';
import TimeSeriesChart from  './TimeSeries.js'
import BarChart from './BarChart.js'

import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';
import OpexpByCategory from './OpexpByCategory'
import CapexpByCategory from "./CapexpByCategory"
import OpexpByModeType from "./OpexpByModeType"
import CapexpByModeType from "./CapexpByModeType"

function App() {

  React.useEffect(() => {
    axios.get('http://localhost:8000/spending_by_budget/?ntd_id=1')
        .then(response => setSpendingByBudget(response.data.data));
    axios.get('http://localhost:8000/spending_by_category/?expense_type=VO,VM,NVM,GA&ntd_id=1')
        .then(response => setOpexpByCategory(response.data.data));
    axios.get('http://localhost:8000/spending_by_category/?expense_type=RS,FC,OC&ntd_id=1')
        .then(response => setCapexpByCategory(response.data.data));
    axios.get('http://localhost:8000/spending_by_mode_type/?expense_type=VO,VM,NVM,GA&ntd_id=1')
        .then(response => setOpexpByModeType(response.data.data));
    axios.get('http://localhost:8000/spending_by_mode_type/?expense_type=RS,FC,OC&ntd_id=1')
        .then(response => setCapexpByModeType(response.data.data));
  }, []);
  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  const [opexpByCategory, setOpexpByCategory] = React.useState(null)
  const [capexpByCategory, setCapexpByCategory] = React.useState(null)
  const [opexpByModeType, setOpexpByModeType] = React.useState(null)
  const [capexpByModeType, setCapexpByModeType] = React.useState(null)

  
        
  return (
    <div className="App">
     
      <body>
        <></>
        <h2>Expense by Budget</h2>
        <SpendingByBudget chartData={spendingByBudget}/>
        <h2>Operating Expense by Type</h2>
        <OpexpByCategory chartData={opexpByCategory}/>
        <h2>Capital Expense by Type</h2>
        <CapexpByCategory chartData={capexpByCategory}/>
        <h2>Operating Expense By Mode Type</h2>
        <OpexpByModeType chartData={opexpByModeType}/>
        <h2>Capital Expense By Mode Type</h2>
        <CapexpByModeType chartData={capexpByModeType}/>
      </body>
    </div>
  );
}

export default App;
