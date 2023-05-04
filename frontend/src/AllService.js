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
        axios.get(`http://localhost:8000/upt_by_service/?t=t${props.params}`)
        .then(response => setUptByService(response.data.data))
        axios.get(`http://localhost:8000/pmt_by_service/?t=t${props.params}`)
        .then(response => setPmtByService(response.data.data))
        axios.get(`http://localhost:8000/vrh_by_service/?t=t${props.params}`)
        .then(response => setVrhByService(response.data.data))
        axios.get(`http://localhost:8000/vrm_by_service/?t=t${props.params}`)
        .then(response => setVrmByService(response.data.data))
        axios.get(`http://localhost:8000/voms_by_service/?t=t${props.params}`)
        .then(response => setVomsByService(response.data.data))
        axios.get(`http://localhost:8000/drm_by_service/?t=t${props.params}`)
        .then(response => setDrmByService(response.data.data))
  
      // axios.get('http://localhost:8000/get_uzas/')
      //   .then(response => setUzaList(response.data));
    }, [props.params]);



  return (
    <div className="service">
      <br/><br/>
    <h1>Passenger Trips</h1>
        <Upt chartData={upt}/>
        <h2>Passenger Trips by Mode Category</h2>
        <UptByModeType chartData={uptByModeType}/>
        <h2>Pasenger Trips by Service</h2>
        <UptByService chartData={uptByService}/>

        <br/><br/>
        <h1>Passenger Miles</h1>
        <Pmt chartData={pmt}/>
        <h2>Passenger Miles by Mode Type</h2>
        <UptByModeType chartData={pmtByModeType}/>
        <h2>Pasenger Miles by Service</h2>
        <UptByService chartData={pmtByService}/>
        <br/><br/>

        <h1>Vehicle Miles</h1>
        <Vrm chartData={vrm}/>
        <h2>Vehicle Miles by Mode Type</h2>
        <UptByModeType chartData={vrmByModeType}/>
        <h2>Vehicle Miles by Service</h2>
        <UptByService chartData={vrmByService}/>
        <br/><br/>


        <h1>Vehicle Hours</h1>
        <Vrh chartData={vrh}/>
        <h2>Vehicle Service Hours by Mode Type</h2>
        <UptByModeType chartData={vrhByModeType}/>
        <h2>Vehicle Hours by Service</h2>
        <UptByService chartData={vrhByService}/>
        <br/><br/>

        <h1>Vehicles Operated in Maximum Service</h1>
        <Voms chartData={voms}/>
        <h2>VOMS by Mode Type</h2>
        <UptByModeType chartData={vomsByModeType}/>
        <h2>VOMS by Service</h2>
        <UptByService chartData={vomsByService}/>


        <br/><br/>
        <h1>Directional Route Miles</h1>
        <Drm chartData={drm}/>
        <h2>Route Miles by Mode Type</h2>
        <UptByModeType chartData={drmByModeType}/>
        <h2>Route Miles by Service</h2>
        <UptByService chartData={drmByService}/>
        
        
        
        
        
        
        
        
        
        
        
        
        
        <br/>
    </div>
  );
}

export default AllService;
