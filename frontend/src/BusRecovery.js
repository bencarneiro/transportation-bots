import './App.css';

import axios from "axios"
import React, { useState } from 'react';



function BusRecovery(props) {




  // const [monthlyUpt, setMonthlyUpt] = React.useState(null)

  React.useEffect(() => {
    if (props.params) {
      // axios.get(`/spending_by_budget/?t=t${props.params}`)
      // .then(response => setSpendingByBudget(response.data.data))
        console.log("hi")
    
        }}


  , [props.params])



  return (
    <div className="expenses">
        <></>
        <h2>UPT last 5 years</h2>
        <h2>UPT M over 2019 M last 5 years</h2>
        <h2>UPT M over 5yr MA M Last 5 years</h2>
        <h2> Vrm last 5 years</h2>
        <h2> VRH last 5 years</h2>
        <h2> VOMS last 5 years</h2>
        <br/>
    </div>
  );
}

export default BusRecovery;
