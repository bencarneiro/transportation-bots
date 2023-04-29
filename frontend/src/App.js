import './App.css';

import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

import axios from "axios"
import React, { useState } from 'react';
import UzaField from "./UzaField"
import StateField from "./StateField"
import AgencyField from "./AgencyField"
import Expenses from './Expenses';
import Service from './Service';
import Performance from './Performance';
import Summary from './Summary';

function App() {



 


  
  const [alignment, setAlignment] = React.useState('summary');
  const [params, setParams] = React.useState("")
  const [uzaParams, setUzaParams] = React.useState("")
  const [stateParams, setStateParams] = React.useState("")
  const [agencyParams, setAgencyParams] = React.useState("")
  const [uzaIds, setUzaIds] = React.useState([])
  const [stateIds, setStateIds] = React.useState([])
  const [agencyIds, setAgencyIds] = React.useState([])

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
  
  const handleChange = (event, newAlignment) => {
    setAlignment(newAlignment);
  };

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
      <ToggleButtonGroup
      size="large"
      color="primary"
      value={alignment}
      exclusive
      onChange={handleChange}
      aria-label="Platform"
    >
      
      <ToggleButton value="summary">Executive Summary</ToggleButton>
      <ToggleButton value="expenses">Expenses</ToggleButton>
      <ToggleButton value="service">Service</ToggleButton>
      <ToggleButton value="performance">Performance</ToggleButton>
    </ToggleButtonGroup>
      <body>
        <></>
        {alignment == "summary" && (
          <Summary params={params}/>
        )}
        {alignment == "expenses" && (
          <Expenses params={params}/>
        )}
        {alignment == "service" && (
          <Service params={params}/>
        )}
        {alignment == "performance" && (
          <Performance params={params}/>
        )}
      </body>
    </div>
  );
}

export default App;
