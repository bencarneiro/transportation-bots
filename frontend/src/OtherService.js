import './App.css';

import axios from "axios"
import React, { useState } from 'react';
import Upt from "./Upt"
import Pmt from "./Pmt"
import Voms from "./Voms"
import Drm from "./Drm"
import Vrm from "./Vrm"
import Vrh from "./Vrh"
import OtherUptByMode from "./OtherUptByMode"
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
        axios.get(`http://localhost:8000/upt/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setUpt(response.data.data));
        axios.get(`http://localhost:8000/pmt/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setPmt(response.data.data));
        axios.get(`http://localhost:8000/vrh/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVrh(response.data.data));
        axios.get(`http://localhost:8000/vrm/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVrm(response.data.data));
        axios.get(`http://localhost:8000/voms/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVoms(response.data.data));
        axios.get(`http://localhost:8000/drm/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setDrm(response.data.data));
        axios.get(`http://localhost:8000/upt_by_mode/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setUptByMode(response.data.data))
        axios.get(`http://localhost:8000/pmt_by_mode/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setPmtByMode(response.data.data))
        axios.get(`http://localhost:8000/vrm_by_mode/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVrmByMode(response.data.data))
        axios.get(`http://localhost:8000/vrh_by_mode/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVrhByMode(response.data.data))
        axios.get(`http://localhost:8000/voms_by_mode/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVomsByMode(response.data.data))
        axios.get(`http://localhost:8000/drm_by_mode/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setDrmByMode(response.data.data))
        axios.get(`http://localhost:8000/upt_by_service/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setUptByService(response.data.data))
        axios.get(`http://localhost:8000/pmt_by_service/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setPmtByService(response.data.data))
        axios.get(`http://localhost:8000/vrh_by_service/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVrhByService(response.data.data))
        axios.get(`http://localhost:8000/vrm_by_service/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVrmByService(response.data.data))
        axios.get(`http://localhost:8000/voms_by_service/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setVomsByService(response.data.data))
        axios.get(`http://localhost:8000/drm_by_service/?mode=FB,OT,AT,nan${props.params}`)
        .then(response => setDrmByService(response.data.data))
    }
  
      // axios.get('http://localhost:8000/get_uzas/')
      //   .then(response => setUzaList(response.data));
    }, [props.params]);



  return (
    <div className="service">
      <br/><br/>
    <h1>Passenger Trips</h1>
        <Upt chartData={upt}/>
        <OtherUptByMode chartData={uptByMode}/>
        <UptByService chartData={uptByService}/>

        <br/><br/>
        <h1>Passenger Miles</h1>
        <Pmt chartData={pmt}/>
        <OtherUptByMode chartData={pmtByMode}/>
        <UptByService chartData={pmtByService}/>
        <br/><br/>

        <h1>Vehicle Miles</h1>
        <Vrm chartData={vrm}/>
        <OtherUptByMode chartData={vrmByMode}/>
        <UptByService chartData={vrmByService}/>
        <br/><br/>


        <h1>Vehicle Hours</h1>
        <Vrh chartData={vrh}/>
        <OtherUptByMode chartData={vrhByMode}/>
        <UptByService chartData={vrhByService}/>
        <br/><br/>

        <h1>Vehicles Operated in Maximum Service</h1>
        <Voms chartData={voms}/>
        <OtherUptByMode chartData={vomsByMode}/>
        <UptByService chartData={vomsByService}/>


        <br/><br/>
        <h1>Directional Route Miles</h1>
        <Drm chartData={drm}/>
        <OtherUptByMode chartData={drmByMode}/>
        <UptByService chartData={drmByService}/>
        
        
        
        
        
        
        
        
        
        
        
        
        
        <br/>
    </div>
  );
}

export default AllService;
