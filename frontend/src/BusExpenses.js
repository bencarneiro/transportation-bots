import './App.css'
import React, { useState } from 'react';
import axios from 'axios';

import SpendingByBudget from './SpendingByBudget';
import OpexpByCategory from './OpexpByCategory'
import CapexpByCategory from "./CapexpByCategory"
import OpexpByMode from "./OpexpByMode"
import CapexpByMode from "./CapexpByMode"
import OpexpByService from './OpexpByService';

function BusExpenses(props) {

  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  const [opexpByCategory, setOpexpByCategory] = React.useState(null)
  const [capexpByCategory, setCapexpByCategory] = React.useState(null)
  const [opexpByMode, setOpexpByMode] = React.useState(null)
  const [capexpByMode, setCapexpByMode] = React.useState(null)
  const [opexpByService, setOpexpByService] = React.useState(null)



  React.useEffect(() => {
    if (props.params) {
    axios.get(`/spending_by_budget/?mode=MB,CB,RB,TB,PB${props.params}`)
      .then(response => setSpendingByBudget(response.data.data));
    axios.get(`/spending_by_category/?mode=MB,CB,RB,TB,PB${props.params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByCategory(response.data.data));
    axios.get(`/spending_by_category/?mode=MB,CB,RB,TB,PB${props.params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByCategory(response.data.data));
    axios.get(`/spending_by_mode/?mode=MB,CB,RB,TB,PB${props.params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByMode(response.data.data));
    axios.get(`/spending_by_mode/?mode=MB,CB,RB,TB,PB${props.params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByMode(response.data.data));
      axios.get(`/opexp_by_service/?mode=MB,CB,RB,TB,PB${props.params}&expense_type=VO,VM,NVM,GA`)
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
        <h2>Operating Expense By Mode</h2>
        <OpexpByMode chartData={opexpByMode} axisLabel={"2024 Dollars"}/>
        <br/>
        <h2>Capital Expense By Mode</h2>
        <CapexpByMode chartData={capexpByMode} axisLabel={"2024 Dollars"}/>
        <br/>
        <h2>Operating Expense By Service</h2>
        <OpexpByService chartData={opexpByService} axisLabel={"2024 Dollars"}/>
        <br/>
    </div>
  );
}

export default BusExpenses;
