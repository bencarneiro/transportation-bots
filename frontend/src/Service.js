import './App.css';

import axios from "axios"
import React, { useState } from 'react';
// import SpendingByBudget from './SpendingByBudget';
// import OpexpByCategory from './OpexpByCategory'
// import CapexpByCategory from "./CapexpByCategory"
// import OpexpByModeType from "./OpexpByModeType"
// import CapexpByModeType from "./CapexpByModeType"
// import OpexpByService from './OpexpByService';

import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
// import AllExpenses from './AllExpenses';
import AllService from './AllService';
import BusService from './BusService';
import RailService from './RailService';
import MicrotransitService from './MicrotransitService';
import FerryService from './FerryService';
import OtherService from './OtherService';

function Service(props) {



  
  const [alignment, setAlignment] = React.useState('all');

  const handleChange = (event, newAlignment) => {
    setAlignment(newAlignment);
  };


  return (
    
    <div className="expenses">
        <br/>
        <ToggleButtonGroup
                size="large"
                color="primary"
                value={alignment}
                exclusive
                onChange={handleChange}
                aria-label="Platform"
                >
                
                <ToggleButton value="all">All Modes</ToggleButton>
                <ToggleButton value="bus">Bus</ToggleButton>
                <ToggleButton value="rail">Rail</ToggleButton>
                <ToggleButton value="microtransit">Micro-Transit</ToggleButton>
                <ToggleButton value="ferry">Ferry</ToggleButton>
                <ToggleButton value="other">Other Modes</ToggleButton>
                </ToggleButtonGroup>
        {alignment == "all" && (
            <AllService params={props.params}/>
        )}
        {alignment == "bus" && (
            <BusService params={props.params}/>
        )}
        {alignment == "rail" && (
            <RailService params={props.params}/>
        )}
        {alignment == "microtransit" && (
            <MicrotransitService params={props.params}/>
        )}
        {alignment == "ferry" && (
            <FerryService params={props.params}/>
        )}
        {alignment == "other" && (
            <OtherService params={props.params}/>
        )}
    </div>
  );
}

export default Service;
