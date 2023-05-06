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
import AllExpenses from './AllExpenses';
import BusExpenses from './BusExpenses';
import RailExpenses from './RailExpenses';
import MicrotransitExpenses from './MicrotransitExpenses';
import FerryExpenses from './FerryExpenses';
import OtherExpenses from './OtherExpenses';


function Expenses(props) {



  
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
                {/* <ToggleButton value="ferry">Ferry</ToggleButton> */}
                <ToggleButton value="other">Other Modes</ToggleButton>
                </ToggleButtonGroup>
        {alignment == "all" && (
            <AllExpenses params={props.params}/>
        )}
        {alignment == "bus" && (
            <BusExpenses params={props.params}/>
        )}
        {alignment == "rail" && (
            <RailExpenses params={props.params}/>
        )}
        {alignment == "microtransit" && (
            <MicrotransitExpenses params={props.params}/>
        )}
        {/* {alignment == "ferry" && (
            <FerryExpenses params={props.params}/>
        )} */}
        {alignment == "other" && (
            <OtherExpenses params={props.params}/>
        )}
        
    </div>
  );
}

export default Expenses;
