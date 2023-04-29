import './App.css';

import axios from "axios"
import React, { useState } from 'react';
import Upt from "./Upt"
import Pmt from "./Pmt"
import Voms from "./Voms"
import Drm from "./Drm"
import Vrm from "./Vrm"
import Vrh from "./Vrh"
import UptByModeType from "./UptByModeType"
import PmtByModeType from './PmtByModeType';
import VrhByModeType from './VrhByModeType';
import VrmByModeType from './VrmByModeType';
import VomsByModeType from './VomsByModeType';
import DrmByModeType from "./DrmByModeType"


function AllService(props) {





    const [upt, setUpt] = React.useState(null)
    const [pmt, setPmt] = React.useState(null)
    const [vrm, setVrm] = React.useState(null)
    const [vrh, setVrh] = React.useState(null)
    const [voms, setVoms] = React.useState(null)
    const [drm, setDrm] = React.useState(null)
    const [uptByModeType, setUptByModeType] = React.useState(null)
    const [pmtByModeType, setPmtByModeType] = React.useState(null)
    const [vrhByModeType, setVrhByModeType] = React.useState(null)
    const [vrmByModeType, setVrmByModeType] = React.useState(null)
    const [vomsByModeType, setVomsByModeType] = React.useState(null)
    const [drmByModeType, setDrmByModeType] = React.useState(null)
  


    React.useEffect(() => {
        axios.get(`http://localhost:8000/upt/?t=t${props.params}`)
        .then(response => setUpt(response.data.data));
        axios.get(`http://localhost:8000/pmt/?t=t${props.params}`)
        .then(response => setPmt(response.data.data));
        axios.get(`http://localhost:8000/vrh/?t=t${props.params}`)
        .then(response => setVrh(response.data.data));
        axios.get(`http://localhost:8000/vrm/?t=t${props.params}`)
        .then(response => setVrm(response.data.data));
        axios.get(`http://localhost:8000/voms/?t=t${props.params}`)
        .then(response => setVoms(response.data.data));
        axios.get(`http://localhost:8000/drm/?t=t${props.params}`)
        .then(response => setDrm(response.data.data));
        axios.get(`http://localhost:8000/upt_by_mode_type/?t=t${props.params}`)
        .then(response => setUptByModeType(response.data.data))
        axios.get(`http://localhost:8000/pmt_by_mode_type/?t=t${props.params}`)
        .then(response => setPmtByModeType(response.data.data))
        axios.get(`http://localhost:8000/vrm_by_mode_type/?t=t${props.params}`)
        .then(response => setVrmByModeType(response.data.data))
        axios.get(`http://localhost:8000/vrh_by_mode_type/?t=t${props.params}`)
        .then(response => setVrhByModeType(response.data.data))
        axios.get(`http://localhost:8000/voms_by_mode_type/?t=t${props.params}`)
        .then(response => setVomsByModeType(response.data.data))
        axios.get(`http://localhost:8000/drm_by_mode_type/?t=t${props.params}`)
        .then(response => setDrmByModeType(response.data.data))
  
      // axios.get('http://localhost:8000/get_uzas/')
      //   .then(response => setUzaList(response.data));
    }, [props]);



  return (
    <div className="service">
       <h2>Passenger Trips</h2>
        <Upt chartData={upt}/>
        <br/>
        <h2>Passenger Miles</h2>
        <Pmt chartData={pmt}/>
        <br/>
        <h2>Vehicles Operated in Maximum Service</h2>
        <Voms chartData={voms}/>
        <br/>
        <h2>Directional Route Miles</h2>
        <Drm chartData={drm}/>
        <br/>
        <h2>Vehicle Miles</h2>
        <Vrm chartData={vrm}/>
        <br/>
        <h2>Vehicle Hours</h2>
        <Vrh chartData={vrh}/>
        <h2>Passengers by Mode Type</h2>
        <UptByModeType chartData={uptByModeType}/>
        <h2>Passenger Miles by Mode Type</h2>
        <PmtByModeType chartData={pmtByModeType}/>
        <h2>Vehicles in Max Service by Mode Type</h2>
        <VomsByModeType chartData={vomsByModeType}/>
        <h2>Route Miles by Mode Type</h2>
        <DrmByModeType chartData={drmByModeType}/>
        <h2>Vehicle Service Hours by Mode Type</h2>
        <VrhByModeType chartData={vrhByModeType}/>
        <h2>Vehicle Service Miles by Mode Type</h2>
        <VrmByModeType chartData={vrmByModeType}/>
        <br/>
    </div>
  );
}

export default AllService;
