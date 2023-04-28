import React from 'react'
import PropTypes from 'prop-types'
// import moment from 'moment'


import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  BarChart,
  Bar,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const moment = require('moment')

const CustomTooltip = ({ active, payload, label }) => {
    // console.log(payload)
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip" style={{backgroundColor: "white", fontSize:"16px", margin:"10px"}}>
        <p className="label">{`Year: ${payload[0].payload.year}`}</p>
        <p className="label">{`Vehicle Operations: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.vehicle_operations)}`}</p>
        <p className="label">{`Vehicle Maintenance: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.vehicle_maintenance)}`}</p>
    <p className="label">{`Non-Vehicle Maintenance: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.non_vehicle_maintenance)}`}</p>
    <p className="label">{`General Administration: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.general_administration)}`}</p>
        </div>
      );
    }
    <YAxis 
    tickFormatter={(value) =>
      new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(value)
    } />
    return null;
  };

const OpexpByCategory = ({ chartData }) => (

    
    <ResponsiveContainer width = '90%' height = {300} >
    <BarChart width={730} height={250} data={chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="year" />
    {/* <XAxis dataKey="expense_type_id_budget"/> */}
    <YAxis 
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          }/>
    {/* <YAxis dataKey={"capexp"}
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          }/> */}
  
            <Tooltip content={<CustomTooltip />} />
    <Legend />
    <Bar dataKey="vehicle_operations" name="Vehicle Operations" fill="Black" />

    <Bar dataKey="vehicle_maintenance" name="Vehicle Maintenance" fill="Red" />
    <Bar dataKey="non_vehicle_maintenance" name="Non-Vehicle Maintenance" fill="Green" />
    <Bar dataKey="general_administration" name="General Administration" fill="Grey" />
    {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
    {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
    {/* <Bar dataKey="year" fill="#82ca9d" /> */}
  </BarChart>
  </ResponsiveContainer>
)

OpexpByCategory.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        expense: PropTypes.number
      })
    ).isRequired
  }

export default OpexpByCategory