import logo from './logo.svg';
import './App.css';
import TimeSeriesChart from './TimeSeries.js'
import BarChart from './BarChart.js'

import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';
import OpexpByCategory from './OpexpByCategory'
import CapexpByCategory from "./CapexpByCategory"
import OpexpByModeType from "./OpexpByModeType"
import CapexpByModeType from "./CapexpByModeType"
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import UzaField from "./UzaField"


function App() {



 


  const [uzaIds, setUzaIds] = React.useState([])
  const [params, setParams] = React.useState("?test=hello")
  const [uzaParams, setUzaParams] = React.useState("")
  const [uzas, setUzas] = React.useState(null)
  const [uzaList, setUzaList] = React.useState([])
  const [agencies, setAgencies] = React.useState([])
  const [states, setStates] = React.useState([])
  const [uzaQ, setUzaQ] = React.useState(null)
  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  const [opexpByCategory, setOpexpByCategory] = React.useState(null)
  const [capexpByCategory, setCapexpByCategory] = React.useState(null)
  const [opexpByModeType, setOpexpByModeType] = React.useState(null)
  const [capexpByModeType, setCapexpByModeType] = React.useState(null)


  React.useEffect(() => {
    axios.get(`http://localhost:8000/spending_by_budget/${params}`)
      .then(response => setSpendingByBudget(response.data.data));
    axios.get(`http://localhost:8000/spending_by_category/${params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByCategory(response.data.data));
    axios.get(`http://localhost:8000/spending_by_category/${params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByCategory(response.data.data));
    axios.get(`http://localhost:8000/spending_by_mode_type/${params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByModeType(response.data.data));
    axios.get(`http://localhost:8000/spending_by_mode_type/${params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByModeType(response.data.data));
    // axios.get('http://localhost:8000/get_uzas/')
    //   .then(response => setUzaList(response.data));
  }, [params]);


  React.useEffect(() => {

    let i = 0;
    let param = "?uza="
    if (uzaIds) {
      while (i < uzaIds.length) {
        param = param.concat(uzaIds[i]['uza'],",")
        i++;
    }
    }
    
    console.log(param)
    if (param !== "&uza=") {
      setUzaParams(param.substring(0,param.length-1)
      )
    } else {
      setUzaParams("")
    }
  }, [uzaIds]);

  React.useEffect(() => {
    setParams(uzaParams)
  }, [uzaParams])


  return (
    <div className="App">
      <header>
        <h1>Search by State, Urbanized Area, or Transit</h1>
        <UzaField setUzaIds={(filters) => { setUzaIds(filters) }} />
        {/* {uzaIds && (
        <h1>{uzaIds.map((val)=><div>{val.uza_name}</div>)}</h1>
      )} */}



      </header>
      <body>
        <></>
        <h2>Expense by Budget</h2>
        <SpendingByBudget chartData={spendingByBudget} />
        <h2>Operating Expense by Type</h2>
        <OpexpByCategory chartData={opexpByCategory} />
        <h2>Capital Expense by Type</h2>
        <CapexpByCategory chartData={capexpByCategory} />
        <h2>Operating Expense By Mode Type</h2>
        <OpexpByModeType chartData={opexpByModeType} />
        <h2>Capital Expense By Mode Type</h2>
        <CapexpByModeType chartData={capexpByModeType} />
      </body>
    </div>
  );
}

export default App;
