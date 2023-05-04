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
import PerformanceByModeType from './PerformanceByModeType';
import PerformanceByService from "./PerformanceByService"

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
  const [costPerUptByModeType, setCostPerUptByModeType] = React.useState(null)
  const [costPerPmtByModeType, setCostPerPmtByModeType] = React.useState(null)
  const [frrByModeType, setFrrByModeType] = React.useState(null)
  const [vrmPerVrhByModeType, setVrmPerVrhByModeType] = React.useState(null)
  const [uptPerVrhByModeType, setUptPerVrhByModeType] = React.useState(null)
  const [uptPerVrmByModeType, setUptPerVrmByModeType] = React.useState(null)
  const [pmtPerVrhByModeType, setPmtPerVrhByModeType] = React.useState(null)
  const [pmtPerVrmByModeType, setPmtPerVrmByModeType] = React.useState(null)
  const [costPerUptByService, setCostPerUptByService] = React.useState(null)
  const [costPerPmtByService, setCostPerPmtByService] = React.useState(null)
  const [frrByService, setFrrByService] = React.useState(null)
  const [vrmPerVrhByService, setVrmPerVrhByService] = React.useState(null)
  const [uptPerVrhByService, setUptPerVrhByService] = React.useState(null)
  const [uptPerVrmByService, setUptPerVrmByService] = React.useState(null)
  const [pmtPerVrhByService, setPmtPerVrhByService] = React.useState(null)
  const [pmtPerVrmByService, setPmtPerVrmByService] = React.useState(null)

  


  React.useEffect(() => {
      axios.get(`http://localhost:8000/cost_per_upt/?t=t${props.params}`)
      .then(response => setCostPerUpt(response.data.data))
      axios.get(`http://localhost:8000/cost_per_pmt/?t=t${props.params}`)
      .then(response => setCostPerPmt(response.data.data))
      // axios.get(`http://localhost:8000/cost_per_vrh/?t=t${props.params}`)
      // .then(response => setCostPerVrh(response.data.data))
      // axios.get(`http://localhost:8000/cost_per_vrm/?t=t${props.params}`)
      // .then(response => setCostPerVrm(response.data.data))
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
      axios.get(`http://localhost:8000/cost_per_upt_by_mode_type/?t=t${props.params}`)
      .then(response => setCostPerUptByModeType(response.data.data))
      axios.get(`http://localhost:8000/cost_per_pmt_by_mode_type/?t=t${props.params}`)
      .then(response => setCostPerPmtByModeType(response.data.data))
      // axios.get(`http://localhost:8000/cost_per_vrh_by_mode_type/?t=t${props.params}`)
      // .then(response => setCostPerVrh(response.data.data))
      // axios.get(`http://localhost:8000/cost_per_vrm_by_mode_type/?t=t${props.params}`)
      // .then(response => setCostPerVrm(response.data.data))
      axios.get(`http://localhost:8000/frr_by_mode_type/?t=t${props.params}`)
      .then(response => setFrrByModeType(response.data.data))
      axios.get(`http://localhost:8000/vrm_per_vrh_by_mode_type/?t=t${props.params}`)
      .then(response => setVrmPerVrhByModeType(response.data.data))
      axios.get(`http://localhost:8000/upt_per_vrh_by_mode_type/?t=t${props.params}`)
      .then(response => setUptPerVrhByModeType(response.data.data))
      axios.get(`http://localhost:8000/upt_per_vrm_by_mode_type/?t=t${props.params}`)
      .then(response => setUptPerVrmByModeType(response.data.data))
      axios.get(`http://localhost:8000/pmt_per_vrh_by_mode_type/?t=t${props.params}`)
      .then(response => setPmtPerVrhByModeType(response.data.data))
      axios.get(`http://localhost:8000/pmt_per_vrm_by_mode_type/?t=t${props.params}`)
      .then(response => setPmtPerVrmByModeType(response.data.data))
      axios.get(`http://localhost:8000/cost_per_upt_by_service/?t=t${props.params}`)
      .then(response => setCostPerUptByService(response.data.data))
      axios.get(`http://localhost:8000/cost_per_pmt_by_service/?t=t${props.params}`)
      .then(response => setCostPerPmtByService(response.data.data))
      // axios.get(`http://localhost:8000/cost_per_vrh_by_service/?t=t${props.params}`)
      // .then(response => setCostPerVrh(response.data.data))
      // axios.get(`http://localhost:8000/cost_per_vrm_by_service/?t=t${props.params}`)
      // .then(response => setCostPerVrm(response.data.data))
      axios.get(`http://localhost:8000/frr_by_service/?t=t${props.params}`)
      .then(response => setFrrByService(response.data.data))
      axios.get(`http://localhost:8000/vrm_per_vrh_by_service/?t=t${props.params}`)
      .then(response => setVrmPerVrhByService(response.data.data))
      axios.get(`http://localhost:8000/upt_per_vrh_by_service/?t=t${props.params}`)
      .then(response => setUptPerVrhByService(response.data.data))
      axios.get(`http://localhost:8000/upt_per_vrm_by_service/?t=t${props.params}`)
      .then(response => setUptPerVrmByService(response.data.data))
      axios.get(`http://localhost:8000/pmt_per_vrh_by_service/?t=t${props.params}`)
      .then(response => setPmtPerVrhByService(response.data.data))
      axios.get(`http://localhost:8000/pmt_per_vrm_by_service/?t=t${props.params}`)
      .then(response => setPmtPerVrmByService(response.data.data))

  }, [props.params]);



  return (
    <div className="App">

        <h2>Cost Per Passenger</h2>
        <CostPerUpt chartData={costPerUpt}/>
        <PerformanceByModeType chartData={costPerUptByModeType}/>
        <PerformanceByService chartData={costPerUptByService}/>
        <br/>
        <h2>Cost Per Passenger Mile</h2>
        <CostPerPmt chartData={costPerPmt}/>
        <PerformanceByModeType chartData={costPerPmtByModeType}/>
        <PerformanceByService chartData={costPerPmtByService}/>
        <br/>
        {/* <h2>Cost Per Vehicle Service Mile</h2>
        <CostPerVrm chartData={costPerVrm}/>
        <br/>
        <h2>Cost Per Vehicle Service Hour</h2>
        <CostPerVrh chartData={costPerVrh}/> */}
        <br/>
        <h2>Fare Recovery Ratio</h2>
        <Frr chartData={frr}/>
        <PerformanceByModeType chartData={frrByModeType}/>
        <PerformanceByService chartData={frrByService}/>
        <br/>
        <h2>Vehicle Miles per Vehicle Hour</h2>
        <VrmPerVrh chartData={vrmPerVrh}/>
        <PerformanceByModeType chartData={vrmPerVrhByModeType}/>
        <PerformanceByService chartData={vrmPerVrhByService}/>
        <br/>
        <h2>Passengers per Service Mile</h2>
        <UptPerVrm chartData={uptPerVrm}/>
        <PerformanceByModeType chartData={uptPerVrmByModeType}/>
        <PerformanceByService chartData={uptPerVrmByService}/>
        <br/>
        <h2>Passengers per Service Hour</h2>
        <UptPerVrh chartData={uptPerVrh}/>
        <PerformanceByModeType chartData={uptPerVrhByModeType}/>
        <PerformanceByService chartData={uptPerVrhByService}/>
        <br/>
        <h2>Passenger Miles per Vehicle Mile</h2>
        <PmtPerVrm chartData={pmtPerVrm}/>
        <PerformanceByModeType chartData={pmtPerVrmByModeType}/>
        <PerformanceByService chartData={pmtPerVrmByService}/>
        <br/>
        <h2>Passenger Miles per Vehicle Hours</h2>
        <PmtPerVrh chartData={pmtPerVrh}/>
        <PerformanceByModeType chartData={pmtPerVrhByModeType}/>
        <PerformanceByService chartData={pmtPerVrhByService}/>
        <br/>
    </div>
  );
}

export default AllPerformance;
