import './App.css';

import axios from "axios"
import React, { useState } from 'react';

import UptMom from "./UptMom";
import UptMomByModeType from "./UptMomByModeType"

import MonthlyUpt from './MonthlyUpt'
import MonthlyUptByModeType from "./MonthlyUptByModeType"

function AllRecovery(props) {


  const [uptMom, setUptMom] = React.useState(null)
  const [uptMomByModeType, setUptMomByModeType] = React.useState(null)

  const [monthlyUpt, setMonthlyUpt] = React.useState(null)
  const [monthlyUptByModeType, setMonthlyUptByModeType] = React.useState(null)
  const [monthlyVrm, setMonthlyVrm] = React.useState(null)
  const [monthlyVrmByModeType, setMonthlyVrmByModeType] = React.useState(null)
  const [monthlyVrh, setMonthlyVrh] = React.useState(null)
  const [monthlyVrhByModeType, setMonthlyVrhByModeType] = React.useState(null)
  // const [monthlyUptPerVrh, setMonthlyUptPerVrh] = React.useState(null)
  // const [monthlyUptPerVrhByModeType, setMonthlyUptPerVrhByModeType] = React.useState(null)

  React.useEffect(() => {
    if (props.params) {
      axios.get(`/upt_month_over_month_baseline/?start=2019-01-01${props.params}`)
      .then(response => setUptMom(response.data.data));
      axios.get(`/upt_month_over_month_baseline_by_mode_type/?start=2019-01-01${props.params}`)
      .then(response => setUptMomByModeType(response.data.data));
      axios.get(`/monthly_upt/?start=2019-01-01${props.params}`)
      .then(response => setMonthlyUpt(response.data.data));
      axios.get(`/monthly_upt_by_mode_type/?start=2019-01-01${props.params}`)
      .then(response => setMonthlyUptByModeType(response.data.data));
      axios.get(`/monthly_vrm/?start=2019-01-01${props.params}`)
      .then(response => setMonthlyVrm(response.data.data));
      axios.get(`/monthly_vrm_by_mode_type/?start=2019-01-01${props.params}`)
      .then(response => setMonthlyVrmByModeType(response.data.data));
      axios.get(`/monthly_vrh/?start=2019-01-01${props.params}`)
      .then(response => setMonthlyVrh(response.data.data));
      axios.get(`/monthly_vrh_by_mode_type/?start=2019-01-01${props.params}`)
      .then(response => setMonthlyVrhByModeType(response.data.data));
      }}


  , [props.params])



  return (
    <div className="recovery">
        <h1>Percentage of Pre-Pandemic Ridership</h1>
        <UptMom chartData={uptMom} axisLabel={"% of Pre-Pandemic Riders"}/>
        <UptMomByModeType chartData={uptMomByModeType} axisLabel={"% of Pre-Pandemic Riders"}/>
        {/* <h1>Riders per Vehicle Hour</h1>
        <MonthlyUpt chartData={monthlyUptPerVrh} axisLabel={'UPT / VRH'} dataKey="upt_per_vrh" lineLabel="Passengers Per Vehicle Hour"/>
        <MonthlyUptByModeType chartData={monthlyUptPerVrhByModeType} axisLabel={"UPT / VRH"}/> */}
        <h1>Ridership</h1>
        <MonthlyUpt chartData={monthlyUpt} axisLabel={'Unlinked Passenger Trips'} dataKey="upt" lineLabel="Unlinked Passenger Trips"/>
        <MonthlyUptByModeType chartData={monthlyUptByModeType} axisLabel={"Unlinked Passenger Trips"}/>
        <h1>Vehicle Miles</h1>
        <MonthlyUpt chartData={monthlyVrm} axisLabel={'Vehicle Revenue Miles'} dataKey="vrm" lineLabel="Vehicle Revenue Miles"/>
        <MonthlyUptByModeType chartData={monthlyVrmByModeType} axisLabel={"Vehicle Revenue Miles"}/>
        <h1>Vehicle Hours</h1>
        <MonthlyUpt chartData={monthlyVrh} axisLabel={'Vehicle Revenue Hours'} dataKey="vrh" lineLabel="Vehicle Revenue Hours"/>
        <MonthlyUptByModeType chartData={monthlyVrhByModeType} axisLabel={"Vehicle Revenue Hours"}/>
        <br/>
    </div>
  );
}

export default AllRecovery;
