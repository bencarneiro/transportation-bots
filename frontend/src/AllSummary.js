import './App.css';

import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';
import UptByModeType from "./UptByModeType"
import PmtByModeType from "./PmtByModeType"
import PerformanceByModeType from "./PerformanceByModeType"
import OpexpByService from "./OpexpByService"
import OpexpByModeType from "./OpexpByModeType"
import CapexpByModeType from "./CapexpByModeType"



function AllSummary(props) {



  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  
  const [uptByModeType, setUptByModeType] = React.useState(null)
  const [pmtByModeType, setPmtByModeType] = React.useState(null)
  //  const [opexpByService, setOpexpByService] = React.useState(null)
  const [opexpByModeType, setOpexpByModeType] = React.useState(null)
  const [capexpByModeType, setCapexpByModeType] = React.useState(null)
  const [costPerUptByModeType, setCostPerUptByModeType] = React.useState(null)
  const [costPerPmtByModeType, setCostPerPmtByModeType] = React.useState(null)

  React.useEffect(() => {
    if (props.params) {
      // axios.get(`http://localhost:8000/spending_by_budget/?t=t${props.params}`)
      // .then(response => setSpendingByBudget(response.data.data))
      axios.get(`http://localhost:8000/upt_by_mode_type/?t=t${props.params}`)
        .then(response => setUptByModeType(response.data.data))
        axios.get(`http://localhost:8000/pmt_by_mode_type/?t=t${props.params}`)
          .then(response => setPmtByModeType(response.data.data))
      axios.get(`http://localhost:8000/cost_per_upt_by_mode_type/?t=t${props.params}`)
        .then(response => setCostPerUptByModeType(response.data.data))
      axios.get(`http://localhost:8000/cost_per_pmt_by_mode_type/?t=t${props.params}`)
        .then(response => setCostPerPmtByModeType(response.data.data))}
        axios.get(`http://localhost:8000/spending_by_mode_type/?t=t${props.params}&expense_type=VO,VM,NVM,GA`)
          .then(response => setOpexpByModeType(response.data.data));
        axios.get(`http://localhost:8000/spending_by_mode_type/?t=t${props.params}&expense_type=RS,FC,OC`)
          .then(response => setCapexpByModeType(response.data.data));

      // axios.get(`http://localhost:8000/opexp_by_service/?t=t${props.params}&expense_type=VO,VM,NVM,GA`)
      // .then(response => setOpexpByService(response.data.data));
      
    }

  , [props.params])



  return (
    <div className="expenses">
        <></>
        <h2>Ridership</h2>
        <UptByModeType chartData={uptByModeType}/>
        <h2>Passenger Miles</h2>
        <PmtByModeType chartData={pmtByModeType}/>
        <h2>Operating Expense</h2>
        <OpexpByModeType chartData={opexpByModeType} />
        <br/>
        <h2>Capital Expense</h2>
        <CapexpByModeType chartData={capexpByModeType} />
        <br/>
        <h2>Cost Per Passenger</h2>
        <PerformanceByModeType chartData={costPerUptByModeType}/>
        <h2>Cost Per Passenger Mile Traveled</h2>
        <PerformanceByModeType chartData={costPerPmtByModeType}/>
        <br/>
        {/* <h2>Spending by Budget</h2>
        <SpendingByBudget chartData={spendingByBudget} />
        <h2>Operating Expense By Service</h2>
        <OpexpByService chartData={opexpByService}/>
        <br/> */}
    </div>
  );
}

export default AllSummary;
