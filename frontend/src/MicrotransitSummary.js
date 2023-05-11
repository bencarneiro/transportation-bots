import './App.css';


import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';
import UptByModeType from "./UptByModeType"
import PmtByModeType from "./PmtByModeType"
import PerformanceByModeType from "./PerformanceByModeType"
import PerformanceByMode from "./PerformanceByMode"
import OpexpByMode from "./OpexpByMode"
import BusUptByMode from "./BusUptByMode"
import MicrotransitPerformanceByMode from "./MicrotransitPerformanceByMode"
import MicrotransitOpexpByMode from "./MicrotransitOpexpByMode"


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
      // axios.get(`/spending_by_budget/?mode=DR,DT,VP,JT${props.params}`)
      // .then(response => setSpendingByBudget(response.data.data))
      axios.get(`/upt_by_mode/?mode=DR,DT,VP,JT${props.params}`)
        .then(response => setUptByMode(response.data.data))
        axios.get(`/pmt_by_mode/?mode=DR,DT,VP,JT${props.params}`)
          .then(response => setPmtByMode(response.data.data))
      axios.get(`/cost_per_upt_by_mode/?mode=DR,DT,VP,JT${props.params}`)
        .then(response => setCostPerUptByMode(response.data.data))
      axios.get(`/cost_per_pmt_by_mode/?mode=DR,DT,VP,JT${props.params}`)
        .then(response => setCostPerPmtByMode(response.data.data))
        axios.get(`/spending_by_mode/?mode=DR,DT,VP,JT${props.params}&expense_type=VO,VM,NVM,GA`)
          .then(response => setOpexpByMode(response.data.data));
        axios.get(`/spending_by_mode/?mode=DR,DT,VP,JT${props.params}&expense_type=RS,FC,OC`)
          .then(response => setCapexpByMode(response.data.data));

      // axios.get(`/opexp_by_service/?mode=DR,DT,VP,JT${props.params}&expense_type=VO,VM,NVM,GA`)
      // .then(response => setOpexpByService(response.data.data));
      
    }}

  , [props.params])



  return (
    <div className="expenses">
        <></>
        <h2>Ridership</h2>
        <MicrotransitPerformanceByMode chartData={uptByMode} axisLabel={"Unlinked Passenger Trips"}/>
        <h2>Passenger Miles</h2>
        <MicrotransitPerformanceByMode chartData={pmtByMode} axisLabel={"Passenger Miles Traveled"}/>
        <h2>Operating Expense</h2>
        <MicrotransitOpexpByMode chartData={opexpByMode} axisLabel={"2022 Dollars"}/>
        <br/>
        <h2>Capital Expense</h2>
        <MicrotransitOpexpByMode chartData={capexpByMode} axisLabel={"2022 Dollars"}/>
        <br/>
        <h2>Cost Per Passenger</h2>
        <MicrotransitPerformanceByMode chartData={costPerUptByMode} axisLabel={"2022 Dollars / Passenger"}/>
        <h2>Cost Per Passenger Mile Traveled</h2>
        <MicrotransitPerformanceByMode chartData={costPerPmtByMode} axisLabel={"2022 Dollars / Mile"}/>
        <br/>
    </div>
  );
}

export default BusSummary;
