import './App.css';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

import React, { useState } from 'react';
import AllRecovery from './AllRecovery';
import BusRecovery from './BusRecovery';
import RailRecovery from './RailRecovery';
import MicrotransitRecovery from './MicrotransitRecovery';
import OtherRecovery from './OtherRecovery';


function Recovery(props) {



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
            <AllRecovery params={props.params} />
        )}
        {alignment == "bus" && (
            <BusRecovery params={props.params} />
        )}
        {alignment == "rail" && (
            <RailRecovery params={props.params} />
        )}
        {alignment == "microtransit" && (
            <MicrotransitRecovery params={props.params} />
        )}
        {alignment == "other" && (
            <OtherRecovery params={props.params} />
        )}
        

        <br/>
    </div>
  );
}

export default Recovery;
