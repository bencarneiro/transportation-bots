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
import UptByService from './UptByService';


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
    const [uptByService, setUptByService] = React.useState(null)
    const [pmtByService, setPmtByService] = React.useState(null)
    const [vrmByService, setVrmByService] = React.useState(null)
    const [vrhByService, setVrhByService] = React.useState(null)
    const [vomsByService, setVomsByService] = React.useState(null)
    const [drmByService, setDrmByService] = React.useState(null)


    React.useEffect(() => {

    if (props.params) {
        axios.get(`/upt/?t=t${props.params}`)
        .then(response => setUpt(response.data.data));
        axios.get(`/pmt/?t=t${props.params}`)
        .then(response => setPmt(response.data.data));
        axios.get(`/vrh/?t=t${props.params}`)
        .then(response => setVrh(response.data.data));
        axios.get(`/vrm/?t=t${props.params}`)
        .then(response => setVrm(response.data.data));
        axios.get(`/voms/?t=t${props.params}`)
        .then(response => setVoms(response.data.data));
        axios.get(`/drm/?t=t${props.params}`)
        .then(response => setDrm(response.data.data));
        axios.get(`/upt_by_mode_type/?t=t${props.params}`)
        .then(response => setUptByModeType(response.data.data))
        axios.get(`/pmt_by_mode_type/?t=t${props.params}`)
        .then(response => setPmtByModeType(response.data.data))
        axios.get(`/vrm_by_mode_type/?t=t${props.params}`)
        .then(response => setVrmByModeType(response.data.data))
        axios.get(`/vrh_by_mode_type/?t=t${props.params}`)
        .then(response => setVrhByModeType(response.data.data))
        axios.get(`/voms_by_mode_type/?t=t${props.params}`)
        .then(response => setVomsByModeType(response.data.data))
        axios.get(`/drm_by_mode_type/?t=t${props.params}`)
        .then(response => setDrmByModeType(response.data.data))
        axios.get(`/upt_by_service/?t=t${props.params}`)
        .then(response => setUptByService(response.data.data))
        axios.get(`/pmt_by_service/?t=t${props.params}`)
        .then(response => setPmtByService(response.data.data))
        axios.get(`/vrh_by_service/?t=t${props.params}`)
        .then(response => setVrhByService(response.data.data))
        axios.get(`/vrm_by_service/?t=t${props.params}`)
        .then(response => setVrmByService(response.data.data))
        axios.get(`/voms_by_service/?t=t${props.params}`)
        .then(response => setVomsByService(response.data.data))
        axios.get(`/drm_by_service/?t=t${props.params}`)
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
        <UptByModeType chartData={uptByModeType} axisLabel={"Unlinked Passenger Trips"}/>
        <UptByService chartData={uptByService} axisLabel={"Unlinked Passenger Trips"}/>

        <br/><br/>
        <h1>Passenger Miles</h1>
        <Pmt chartData={pmt} axisLabel={"Passenger Miles Travled"}/>
        <UptByModeType chartData={pmtByModeType} axisLabel={"Passenger Miles Travled"}/>
        <UptByService chartData={pmtByService} axisLabel={"Passenger Miles Travled"}/>
        <br/><br/>

        <h1>Vehicle Miles</h1>
        <Vrm chartData={vrm} axisLabel={"Vehicle Revenue Miles"}/>
        <UptByModeType chartData={vrmByModeType} axisLabel={"Vehicle Revenue Miles"}/>
        <UptByService chartData={vrmByService} axisLabel={"Vehicle Revenue Miles"}/>
        <br/><br/>


        <h1>Vehicle Hours</h1>
        <Vrh chartData={vrh} axisLabel={"Vehicle Revenue Hours"}/>
        <UptByModeType chartData={vrhByModeType} axisLabel={"Vehicle Revenue Hours"}/>
        <UptByService chartData={vrhByService} axisLabel={"Vehicle Revenue Hours"}/>
        <br/><br/>

        <h1>Vehicles Operated in Maximum Service</h1>
        <Voms chartData={voms} axisLabel={"Vehicles at Max Service"}/>
        <UptByModeType chartData={vomsByModeType} axisLabel={"Vehicles at Max Service"}/>
        <UptByService chartData={vomsByService} axisLabel={"Vehicles at Max Service"}/>


        <br/><br/>
        <h1>Directional Route Miles</h1>
        <Drm chartData={drm} axisLabel={"Directional Route Miles"}/>
        <UptByModeType chartData={drmByModeType} axisLabel={"Directional Route Miles"}/>
        <UptByService chartData={drmByService} axisLabel={"Directional Route Miles"}/>
        
        
        
        
        
        
        
        
        
        
        
        
        
        <br/>
    </div>
  );
}

export default AllService;
