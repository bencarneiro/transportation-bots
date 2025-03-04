import './App.css';

import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';
import OpexpByCategory from './OpexpByCategory'
import CapexpByCategory from "./CapexpByCategory"
import OpexpByModeType from "./OpexpByModeType"
import CapexpByModeType from "./CapexpByModeType"
import OpexpByService from './OpexpByService';


function AllExpenses(props) {



  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  const [opexpByCategory, setOpexpByCategory] = React.useState(null)
  const [capexpByCategory, setCapexpByCategory] = React.useState(null)
  const [opexpByModeType, setOpexpByModeType] = React.useState(null)
  const [capexpByModeType, setCapexpByModeType] = React.useState(null)
  const [opexpByService, setOpexpByService] = React.useState(null)

  


  React.useEffect(() => {
    if (props.params) {
    axios.get(`/spending_by_budget/?t=t${props.params}`)
      .then(response => setSpendingByBudget(response.data.data));
    axios.get(`/spending_by_category/?t=t${props.params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByCategory(response.data.data));
    axios.get(`/spending_by_category/?t=t${props.params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByCategory(response.data.data));
    axios.get(`/spending_by_mode_type/?t=t${props.params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByModeType(response.data.data));
    axios.get(`/spending_by_mode_type/?t=t${props.params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByModeType(response.data.data));
      axios.get(`/opexp_by_service/?t=t${props.params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByService(response.data.data));}
    }
  , [props.params])



  return (
    <div className="expenses">
        <></>
        <h2>Expense by Budget</h2>
        <SpendingByBudget chartData={spendingByBudget}  axisLabel={"2024 Dollars"}/>
        <br/>
        <h2>Operating Expense by Category</h2>
        <OpexpByCategory chartData={opexpByCategory} axisLabel={"2024 Dollars"}/>
        <br/>
        <h2>Capital Expense by Category</h2>
        <CapexpByCategory chartData={capexpByCategory} axisLabel={"2024 Dollars"}/>
        <br/>
        <h2>Operating Expense By Mode Type</h2>
        <OpexpByModeType chartData={opexpByModeType} axisLabel={"2024 Dollars"}/>
        <br/>
        <h2>Capital Expense By Mode Type</h2>
        <CapexpByModeType chartData={capexpByModeType} axisLabel={"2024 Dollars"}/>
        <br/>
        <h2>Operating Expense By Service</h2>
        <OpexpByService chartData={opexpByService} axisLabel={"2024 Dollars"}/>
        <br/>
    </div>
  );
}

export default AllExpenses;
