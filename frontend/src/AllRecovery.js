import './App.css';

import axios from "axios"
import React, { useState } from 'react';

import UptMom from "./UptMom";
import UptMomByModeType from "./UptMomByModeType"

function AllRecovery(props) {


  const [uptMom, setUptMom] = React.useState(null)
  const [uptMomByModeType, setUptMomByModeType] = React.useState(null)

  // const [monthlyUpt, setMonthlyUpt] = React.useState(null)

  React.useEffect(() => {
    if (props.params) {
      axios.get(`http://127.0.0.1:8000/upt_month_over_month_baseline/?t=t${props.params}`)
      .then(response => setUptMom(response.data.data));
      axios.get(`http://127.0.0.1:8000/upt_month_over_month_baseline_by_mode_type/?t=t${props.params}`)
      .then(response => setUptMomByModeType(response.data.data));
    
    
        }}


  , [props.params])



  return (
    <div className="expenses">
        <></>
        <></>
        {/* # Change in Ridership Month over Month by mode type
        UPT by mode type
        upt by service
        # Change in VRM Month over Month by mode type
        vrm by mode type
        vrm by service
        # Change in VRH Month over Month by mode type
        vrh by mode type
        vrh by service */}
        <h1>Percentage of Pre-Pandemic Ridership</h1>
        <UptMom chartData={uptMom} axisLabel={"% of Pre-Pandemic Riders"}/>
        <UptMomByModeType chartData={uptMomByModeType} axisLabel={"% of Pre-Pandemic Riders"}/>
        <h2>UPT M over 2019 M last 5 years By mode type</h2>
        <h2>UPT M over 5yr MA M Last 5 years By mode type</h2>
        <h2>UPT last 5 years By mode type</h2>
        <h2> Vrm last 5 years By mode type</h2>
        <h2> VRH last 5 years By mode type</h2>
        <h2> VOMS last 5 years By mode type</h2>
        <br/>
    </div>
  );
}

export default AllRecovery;
