import './App.css';


import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';
import UptByModeType from "./UptByModeType"
import PmtByModeType from "./PmtByModeType"
import PerformanceByModeType from "./PerformanceByModeType"
// import RailPerformanceByMode from "./RailPerformanceByMode"
import RailOpexpByMode from "./RailOpexpByMode"
import RailPerformanceByMode from "./RailPerformanceByMode"


function BusSummary(props) {



  // const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  
  const [uptByMode, setUptByMode] = React.useState(null)
  const [pmtByMode, setPmtByMode] = React.useState(null)
  //  const [opexpByService, setOpexpByService] = React.useState(null)
  const [opexpByMode, setOpexpByMode] = React.useState(null)
  const [capexpByMode, setCapexpByMode] = React.useState(null)
  const [costPerUptByMode, setCostPerUptByMode] = React.useState(null)
  const [costPerPmtByMode, setCostPerPmtByMode] = React.useState(null)

  React.useEffect(() => {
    if (props.params) {
      // axios.get(`http://localhost:8000/spending_by_budget/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}`)
      // .then(response => setSpendingByBudget(response.data.data))
      axios.get(`http://localhost:8000/upt_by_mode/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}`)
        .then(response => setUptByMode(response.data.data))
        axios.get(`http://localhost:8000/pmt_by_mode/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}`)
          .then(response => setPmtByMode(response.data.data))
      axios.get(`http://localhost:8000/cost_per_upt_by_mode/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}`)
        .then(response => setCostPerUptByMode(response.data.data))
      axios.get(`http://localhost:8000/cost_per_pmt_by_mode/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}`)
        .then(response => setCostPerPmtByMode(response.data.data))
        axios.get(`http://localhost:8000/spending_by_mode/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}&expense_type=VO,VM,NVM,GA`)
          .then(response => setOpexpByMode(response.data.data));
        axios.get(`http://localhost:8000/spending_by_mode/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}&expense_type=RS,FC,OC`)
          .then(response => setCapexpByMode(response.data.data));

      // axios.get(`http://localhost:8000/opexp_by_service/?mode=LR,CR,HR,YR,SR,OR,MG,AR,IP,CC${props.params}&expense_type=VO,VM,NVM,GA`)
      // .then(response => setOpexpByService(response.data.data));
      
    }}

  , [props.params])



  return (
    <div className="expenses">
        <></>
        <h2>Ridership</h2>
        <RailPerformanceByMode chartData={uptByMode}/>
        <h2>Passenger Miles</h2>
        <RailPerformanceByMode chartData={pmtByMode}/>
        <h2>Operating Expense</h2>
        <RailOpexpByMode chartData={opexpByMode} />
        <br/>
        <h2>Capital Expense</h2>
        <RailOpexpByMode chartData={capexpByMode} />
        <br/>
        <h2>Cost Per Passenger</h2>
        <RailPerformanceByMode chartData={costPerUptByMode}/>
        <h2>Cost Per Passenger Mile Traveled</h2>
        <RailPerformanceByMode chartData={costPerPmtByMode}/>
        <br/>
    </div>
  );
}

export default BusSummary;
