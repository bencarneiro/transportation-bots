import './App.css';

import axios from "axios"
import React, { useState } from 'react';
import CostPerUpt from './CostPerUpt';
import CostPerPmt from './CostPerPmt';
import CostPerVrh from './CostPerVrh';
import CostPerVrm from './CostPerVrm';
import Frr from './Frr';
import VrmPerVrh from './VrmPerVrh';
import PmtPerVrh from './PmtPerVrh';
import PmtPerVrm from './PmtPerVrm';
import UptPerVrh from './UptPerVrh';
import UptPerVrm from './UptPerVrm';

function AllPerformance(props) {

  const [costPerUpt, setCostPerUpt] = React.useState(null)
  const [costPerPmt, setCostPerPmt] = React.useState(null)
  const [costPerVrh, setCostPerVrh] = React.useState(null)
  const [costPerVrm, setCostPerVrm] = React.useState(null)
  const [frr, setFrr] = React.useState(null)
  const [vrmPerVrh, setVrmPerVrh] = React.useState(null)
  const [uptPerVrh, setUptPerVrh] = React.useState(null)
  const [uptPerVrm, setUptPerVrm] = React.useState(null)
  const [pmtPerVrh, setPmtPerVrh] = React.useState(null)
  const [pmtPerVrm, setPmtPerVrm] = React.useState(null)
  


  React.useEffect(() => {
      axios.get(`http://localhost:8000/cost_per_upt/?t=t${props.params}`)
      .then(response => setCostPerUpt(response.data.data))
      axios.get(`http://localhost:8000/cost_per_pmt/?t=t${props.params}`)
      .then(response => setCostPerPmt(response.data.data))
      axios.get(`http://localhost:8000/cost_per_vrh/?t=t${props.params}`)
      .then(response => setCostPerVrh(response.data.data))
      axios.get(`http://localhost:8000/cost_per_vrm/?t=t${props.params}`)
      .then(response => setCostPerVrm(response.data.data))
      axios.get(`http://localhost:8000/frr/?t=t${props.params}`)
      .then(response => setFrr(response.data.data))
      axios.get(`http://localhost:8000/vrm_per_vrh/?t=t${props.params}`)
      .then(response => setVrmPerVrh(response.data.data))
      axios.get(`http://localhost:8000/upt_per_vrh/?t=t${props.params}`)
      .then(response => setUptPerVrh(response.data.data))
      axios.get(`http://localhost:8000/upt_per_vrm/?t=t${props.params}`)
      .then(response => setUptPerVrm(response.data.data))
      axios.get(`http://localhost:8000/pmt_per_vrh/?t=t${props.params}`)
      .then(response => setPmtPerVrh(response.data.data))
      axios.get(`http://localhost:8000/pmt_per_vrm/?t=t${props.params}`)
      .then(response => setPmtPerVrm(response.data.data))

  }, [props]);



  return (
    <div className="App">

        <h2>Cost Per Passenger</h2>
        <CostPerUpt chartData={costPerUpt}/>
        <br/>
        <h2>Cost Per Passenger Mile</h2>
        <CostPerPmt chartData={costPerPmt}/>
        <br/>
        <h2>Cost Per Vehicle Service Mile</h2>
        <CostPerVrm chartData={costPerVrm}/>
        <br/>
        <h2>Cost Per Vehicle Service Hour</h2>
        <CostPerVrh chartData={costPerVrh}/>
        <br/>
        <h2>Fare Recovery Ratio</h2>
        <Frr chartData={frr}/>
        <br/>
        <h2>Vehicle Miles per Vehicle Hour</h2>
        <VrmPerVrh chartData={vrmPerVrh}/>
        <br/>
        <h2>Passengers per Service Mile</h2>
        <UptPerVrm chartData={uptPerVrm}/>
        <br/>
        <h2>Passengers per Service Hour</h2>
        <UptPerVrh chartData={uptPerVrh}/>
        <br/>
        <h2>Passenger Miles per Vehicle Mile</h2>
        <PmtPerVrm chartData={pmtPerVrm}/>
        <br/>
        <h2>Passenger Miles per Vehicle Hours</h2>
        <PmtPerVrh chartData={pmtPerVrh}/>
        <br/>
    </div>
  );
}

export default AllPerformance;
