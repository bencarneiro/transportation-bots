import './App.css';

import axios from "axios"
import React, { useState } from 'react';
import Upt from "./Upt"
import Pmt from "./Pmt"
import Voms from "./Voms"
import Drm from "./Drm"
import Vrm from "./Vrm"
import Vrh from "./Vrh"
import MicrotransitUptByMode from "./MicrotransitUptByMode"
import UptByService from './UptByService';


function AllService(props) {





    const [upt, setUpt] = React.useState(null)
    const [pmt, setPmt] = React.useState(null)
    const [vrm, setVrm] = React.useState(null)
    const [vrh, setVrh] = React.useState(null)
    const [voms, setVoms] = React.useState(null)
    const [drm, setDrm] = React.useState(null)
    const [uptByMode, setUptByMode] = React.useState(null)
    const [pmtByMode, setPmtByMode] = React.useState(null)
    const [vrhByMode, setVrhByMode] = React.useState(null)
    const [vrmByMode, setVrmByMode] = React.useState(null)
    const [vomsByMode, setVomsByMode] = React.useState(null)
    const [drmByMode, setDrmByMode] = React.useState(null)
    const [uptByService, setUptByService] = React.useState(null)
    const [pmtByService, setPmtByService] = React.useState(null)
    const [vrmByService, setVrmByService] = React.useState(null)
    const [vrhByService, setVrhByService] = React.useState(null)
    const [vomsByService, setVomsByService] = React.useState(null)
    const [drmByService, setDrmByService] = React.useState(null)


    React.useEffect(() => {

    if (props.params) {
        axios.get(`/upt/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setUpt(response.data.data));
        axios.get(`/pmt/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setPmt(response.data.data));
        axios.get(`/vrh/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVrh(response.data.data));
        axios.get(`/vrm/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVrm(response.data.data));
        axios.get(`/voms/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVoms(response.data.data));
        axios.get(`/drm/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setDrm(response.data.data));
        axios.get(`/upt_by_mode/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setUptByMode(response.data.data))
        axios.get(`/pmt_by_mode/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setPmtByMode(response.data.data))
        axios.get(`/vrm_by_mode/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVrmByMode(response.data.data))
        axios.get(`/vrh_by_mode/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVrhByMode(response.data.data))
        axios.get(`/voms_by_mode/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVomsByMode(response.data.data))
        axios.get(`/drm_by_mode/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setDrmByMode(response.data.data))
        axios.get(`/upt_by_service/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setUptByService(response.data.data))
        axios.get(`/pmt_by_service/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setPmtByService(response.data.data))
        axios.get(`/vrh_by_service/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVrhByService(response.data.data))
        axios.get(`/vrm_by_service/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVrmByService(response.data.data))
        axios.get(`/voms_by_service/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setVomsByService(response.data.data))
        axios.get(`/drm_by_service/?mode=DT,DR,VP,JT${props.params}`)
        .then(response => setDrmByService(response.data.data))
    }
  
      // axios.get('http://localhost:8000/get_uzas/')
      //   .then(response => setUzaList(response.data));
    }, [props.params]);



  return (
    <div className="service">
      <br/><br/>
    <h1>Passenger Trips</h1>
        <Upt chartData={upt} axisLabel={"Unlinked Passenger Trips"}/>
        <MicrotransitUptByMode chartData={uptByMode} axisLabel={"Unlinked Passenger Trips"}/>
        <UptByService chartData={uptByService} axisLabel={"Unlinked Passenger Trips"}/>

        <br/><br/>
        <h1>Passenger Miles</h1>
        <Pmt chartData={pmt} axisLabel={"Passenger Miles Travled"}/>
        <MicrotransitUptByMode chartData={pmtByMode} axisLabel={"Passenger Miles Travled"}/>
        <UptByService chartData={pmtByService} axisLabel={"Passenger Miles Travled"}/>
        <br/><br/>

        <h1>Vehicle Miles</h1>
        <Vrm chartData={vrm} axisLabel={"Vehicle Revenue Miles"}/>
        <MicrotransitUptByMode chartData={vrmByMode} axisLabel={"Vehicle Revenue Miles"}/>
        <UptByService chartData={vrmByService} axisLabel={"Vehicle Revenue Miles"}/>
        <br/><br/>


        <h1>Vehicle Hours</h1>
        <Vrh chartData={vrh} axisLabel={"Vehicle Revenue Hours"}/>
        <MicrotransitUptByMode chartData={vrhByMode} axisLabel={"Vehicle Revenue Hours"}/>
        <UptByService chartData={vrhByService} axisLabel={"Vehicle Revenue Hours"}/>
        <br/><br/>

        <h1>Vehicles Operated in Maximum Service</h1>
        <Voms chartData={voms} axisLabel={"Vehicles at Max Service"}/>
        <MicrotransitUptByMode chartData={vomsByMode} axisLabel={"Vehicles at Max Service"}/>
        <UptByService chartData={vomsByService} axisLabel={"Vehicles at Max Service"}/>


        <br/><br/>
        <h1>Directional Route Miles</h1>
        <Drm chartData={drm} axisLabel={"Directional Route Miles"}/>
        <MicrotransitUptByMode chartData={drmByMode} axisLabel={"Directional Route Miles"}/>
        <UptByService chartData={drmByService} axisLabel={"Directional Route Miles"}/>
        
        
        
        
        
        
        
        
        
        
        
        
        
        <br/>
    </div>
  );
}

export default AllService;
