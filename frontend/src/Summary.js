import './App.css';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

import axios from "axios"
import React, { useState } from 'react';
import SpendingByBudget from './SpendingByBudget';
import AllSummary from './AllSummary';
import BusSummary from './BusSummary';
import RailSummary from './RailSummary';
import MicrotransitSummary from './MicrotransitSummary';
import OtherSummary from './OtherSummary';
import FerrySummary from './FerrySummary';


function Summary(props) {



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
            <AllSummary params={props.params} />
        )}
        {alignment == "bus" && (
            <BusSummary params={props.params} />
        )}
        {alignment == "rail" && (
            <RailSummary params={props.params} />
        )}
        {alignment == "microtransit" && (
            <MicrotransitSummary params={props.params} />
        )}
        {/* {alignment == "ferry" && (
            <FerrySummary params={props.params} />
        )} */}
        {alignment == "other" && (
            <OtherSummary params={props.params} />
        )}
        

        <br/>
    </div>
  );
}

export default Summary;
