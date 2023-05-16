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
import MonthlyUpt from './MonthlyUpt';



function AllSummary(props) {



  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  
  const [uptByModeType, setUptByModeType] = React.useState(null)
  const [pmtByModeType, setPmtByModeType] = React.useState(null)
  //  const [opexpByService, setOpexpByService] = React.useState(null)
  const [opexpByModeType, setOpexpByModeType] = React.useState(null)
  const [capexpByModeType, setCapexpByModeType] = React.useState(null)
  const [costPerUptByModeType, setCostPerUptByModeType] = React.useState(null)
  const [costPerPmtByModeType, setCostPerPmtByModeType] = React.useState(null)
  // const [monthlyUpt, setMonthlyUpt] = React.useState(null)

  React.useEffect(() => {
    if (props.params) {
      // axios.get(`/spending_by_budget/?t=t${props.params}`)
      // .then(response => setSpendingByBudget(response.data.data))
      axios.get(`/upt_by_mode_type/?t=t${props.params}`)
        .then(response => setUptByModeType(response.data.data))
        axios.get(`/pmt_by_mode_type/?t=t${props.params}`)
          .then(response => setPmtByModeType(response.data.data))
      axios.get(`/cost_per_upt_by_mode_type/?t=t${props.params}`)
        .then(response => setCostPerUptByModeType(response.data.data))
      axios.get(`/cost_per_pmt_by_mode_type/?t=t${props.params}`)
        .then(response => setCostPerPmtByModeType(response.data.data))
        axios.get(`/spending_by_mode_type/?t=t${props.params}&expense_type=VO,VM,NVM,GA`)
          .then(response => setOpexpByModeType(response.data.data));
        axios.get(`/spending_by_mode_type/?t=t${props.params}&expense_type=RS,FC,OC`)
          .then(response => setCapexpByModeType(response.data.data));}}

        // axios.get(`http://127.0.0.1:8000/monthly_upt/?t=t${props.params}`)
        // .then(response => setMonthlyUpt(response.data.data));}

      // axios.get(`/opexp_by_service/?t=t${props.params}&expense_type=VO,VM,NVM,GA`)
      // .then(response => setOpexpByService(response.data.data));
      
    

  , [props.params])



  return (
    <div className="expenses">
        <></>
        <h2>Ridership</h2>
        <UptByModeType chartData={uptByModeType} axisLabel={"Unlinked Passenger Trips"}/>
        <h2>Passenger Miles</h2>
        <PmtByModeType chartData={pmtByModeType} axisLabel={"Passenger Miles Traveled"}/>
        <h2>Operating Expense</h2>
        <OpexpByModeType chartData={opexpByModeType} axisLabel={"2022 Dollars"} />
        <br/>
        <h2>Capital Expense</h2>
        <CapexpByModeType chartData={capexpByModeType} axisLabel={"2022 Dollars"} />
        <br/>
        <h2>Cost Per Passenger</h2>
        <PerformanceByModeType chartData={costPerUptByModeType} axisLabel={"2022 Dollars / Passenger"}/>
        <h2>Cost Per Passenger Mile Traveled</h2>
        <PerformanceByModeType chartData={costPerPmtByModeType} axisLabel={"2022 Dollars / Mile"}/>
        {/* <h2>Monthly Ridership</h2>
        <MonthlyUpt chartData={monthlyUpt} axisLabel={'Unlinked Passenger Trips'}/> */}
        <br/>
    </div>
  );
}

export default AllSummary;
