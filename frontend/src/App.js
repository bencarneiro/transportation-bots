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
import StateField from "./StateField"
import AgencyField from "./AgencyField"


function App() {



 


  const [uzaIds, setUzaIds] = React.useState([])
  const [params, setParams] = React.useState("")
  const [uzaParams, setUzaParams] = React.useState("")
  const [stateParams, setStateParams] = React.useState("")
  const [agencyParams, setAgencyParams] = React.useState("")
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
  const [stateIds, setStateIds] = React.useState([])
  const [agencyIds, setAgencyIds] = React.useState([])


  React.useEffect(() => {
    axios.get(`http://localhost:8000/spending_by_budget/?t=t${params}`)
      .then(response => setSpendingByBudget(response.data.data));
    axios.get(`http://localhost:8000/spending_by_category/?t=t${params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByCategory(response.data.data));
    axios.get(`http://localhost:8000/spending_by_category/?t=t${params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByCategory(response.data.data));
    axios.get(`http://localhost:8000/spending_by_mode_type/?t=t${params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByModeType(response.data.data));
    axios.get(`http://localhost:8000/spending_by_mode_type/?t=t${params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByModeType(response.data.data));
    // axios.get('http://localhost:8000/get_uzas/')
    //   .then(response => setUzaList(response.data));
  }, [params]);


  React.useEffect(() => {

    let i = 0;
    let param = "&uza="
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

    let i = 0;
    let param = "&state="
    if (stateIds) {
      while (i < stateIds.length) {
        param = param.concat(stateIds[i]['state'],",")
        i++;
    }
    }
    
    console.log(param)
    if (param !== "&state=") {
      setStateParams(param.substring(0,param.length-1)
      )
    } else {
      setStateParams("")
    }
  }, [stateIds]);


  React.useEffect(() => {

    let i = 0;
    let param = "&agency="
    if (agencyIds) {
      while (i < agencyIds.length) {
        param = param.concat(agencyIds[i]['id'],",")
        i++;
    }
    }
    
    console.log(param)
    if (param !== "&agency=") {
      setAgencyParams(param.substring(0,param.length-1)
      )
    } else {
      setAgencyParams("")
    }
  }, [agencyIds]);


  React.useEffect(() => {
    console.log(uzaParams.concat(stateParams,agencyParams))
    setParams(uzaParams.concat(stateParams,agencyParams))
  }, [uzaParams, stateParams, agencyParams])
  


  return (
    <div className="App">
      <header>
        <h1>Explore Transit Spending</h1>
        <br/>
        <UzaField setUzaIds={(filters) => { setUzaIds(filters) }} />
        <br/>
        <StateField setStateIds={(filters) => { setStateIds(filters) }} />
        <br/>
        <AgencyField setAgencyIds={(filters) => {setAgencyIds(filters)}}/>
        <br/>
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
