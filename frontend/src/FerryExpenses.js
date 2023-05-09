import './App.css'
import React, { useState } from 'react';
import axios from 'axios';

import SpendingByBudget from './SpendingByBudget';
import OpexpByCategory from './OpexpByCategory'
import CapexpByCategory from "./CapexpByCategory"
import OpexpByService from './OpexpByService';

function BusExpenses(props) {

  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  const [opexpByCategory, setOpexpByCategory] = React.useState(null)
  const [capexpByCategory, setCapexpByCategory] = React.useState(null)
  const [opexpByService, setOpexpByService] = React.useState(null)



  React.useEffect(() => {
    if (props.params) {
    axios.get(`http://45.33.31.186/spending_by_budget/?mode=FB${props.params}`)
      .then(response => setSpendingByBudget(response.data.data));
    axios.get(`http://45.33.31.186/spending_by_category/?mode=FB${props.params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByCategory(response.data.data));
    axios.get(`http://45.33.31.186/spending_by_category/?mode=FB${props.params}&expense_type=RS,FC,OC`)
      .then(response => setCapexpByCategory(response.data.data));
      axios.get(`http://45.33.31.186/opexp_by_service/?mode=FB${props.params}&expense_type=VO,VM,NVM,GA`)
      .then(response => setOpexpByService(response.data.data));}
    }
  , [props.params])

  return (
    <div className="expenses">
        <></>
        <h2>Expense by Budget</h2>
        <SpendingByBudget chartData={spendingByBudget} />
        <br/>
        <h2>Operating Expense by Category</h2>
        <OpexpByCategory chartData={opexpByCategory} />
        <br/>
        <h2>Capital Expense by Category</h2>
        <CapexpByCategory chartData={capexpByCategory} />
        <br/>
        <h2>Operating Expense By Service</h2>
        <OpexpByService chartData={opexpByService}/>
        <br/>
    </div>
  );
}

export default BusExpenses;
