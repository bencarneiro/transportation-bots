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
import OpexpByService from './OpexpByService';
import Upt from "./Upt"
import Pmt from "./Pmt"
import Voms from "./Voms"
import Drm from "./Drm"
import Vrm from "./Vrm"
import Vrh from "./Vrh"


function App() {



 


  
  const [params, setParams] = React.useState("")
  const [uzaParams, setUzaParams] = React.useState("")
  const [stateParams, setStateParams] = React.useState("")
  const [agencyParams, setAgencyParams] = React.useState("")
  const [uzaIds, setUzaIds] = React.useState([])
  const [stateIds, setStateIds] = React.useState([])
  const [agencyIds, setAgencyIds] = React.useState([])
  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  const [opexpByCategory, setOpexpByCategory] = React.useState(null)
  const [capexpByCategory, setCapexpByCategory] = React.useState(null)
  const [opexpByModeType, setOpexpByModeType] = React.useState(null)
  const [capexpByModeType, setCapexpByModeType] = React.useState(null)
  const [opexpByService, setOpexpByService] = React.useState(null)
  const [upt, setUpt] = React.useState(null)
  const [pmt, setPmt] = React.useState(null)
  const [vrm, setVrm] = React.useState(null)
  const [vrh, setVrh] = React.useState(null)
  const [voms, setVoms] = React.useState(null)
  const [drm, setDrm] = React.useState(null)
  


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
      axios.get(`http://localhost:8000/opexp_by_service/?t=t${params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByService(response.data.data));
      axios.get(`http://localhost:8000/upt/?t=t${params}`)
      .then(response => setUpt(response.data.data));
      axios.get(`http://localhost:8000/pmt/?t=t${params}`)
      .then(response => setPmt(response.data.data));
      axios.get(`http://localhost:8000/vrh/?t=t${params}`)
      .then(response => setVrh(response.data.data));
      axios.get(`http://localhost:8000/vrm/?t=t${params}`)
      .then(response => setVrm(response.data.data));
      axios.get(`http://localhost:8000/voms/?t=t${params}`)
      .then(response => setVoms(response.data.data));
      axios.get(`http://localhost:8000/drm/?t=t${params}`)
      .then(response => setDrm(response.data.data));

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
        <br/>
        <h2>Operating Expense by Type</h2>
        <OpexpByCategory chartData={opexpByCategory} />
        <br/>
        <h2>Capital Expense by Type</h2>
        <CapexpByCategory chartData={capexpByCategory} />
        <br/>
        <h2>Operating Expense By Mode Type</h2>
        <OpexpByModeType chartData={opexpByModeType} />
        <br/>
        <h2>Capital Expense By Mode Type</h2>
        <CapexpByModeType chartData={capexpByModeType} />
        <br/>
        <h2>Operating Expense By Service</h2>
        <OpexpByService chartData={opexpByService}/>
        <br/>
        <h2>Passenger Trips</h2>
        <Upt chartData={upt}/>
        <br/>
        <h2>Passenger Miles</h2>
        <Pmt chartData={pmt}/>
        <br/>
        <h2>Vehicles Operated in Maximum Service</h2>
        <Voms chartData={voms}/>
        <br/>
        <h2>Directional Route Miles</h2>
        <Drm chartData={drm}/>
        <br/>
        <h2>Vehicle Miles</h2>
        <Vrm chartData={vrm}/>
        <br/>
        <h2>Vehicle Hours</h2>
        <Vrh chartData={vrh}/>
        <br/>
      </body>
    </div>
  );
}

export default App;
