import './App.css';

import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';

function AllSummary(props) {



  const [spendingByBudget, setSpendingByBudget] = React.useState(null)
  


  React.useEffect(() => {
    if (props.params) {
      axios.get(`http://localhost:8000/spending_by_budget/?t=t${props.params}`)
      .then(response => setSpendingByBudget(response.data.data));}
    }

  , [props.params])



  return (
    <div className="expenses">
        <></>
        <h2>Expense by Budget</h2>
        <SpendingByBudget chartData={spendingByBudget} />
        <br/>
    </div>
  );
}

export default AllSummary;
