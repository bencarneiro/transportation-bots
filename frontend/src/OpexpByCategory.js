import React from 'react'
import PropTypes from 'prop-types'
// import moment from 'moment'


import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Line,
  LineChart,
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
        <h3 className="label">{`${payload[0].payload.year}`}</h3>
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

    return null;
  };

const OpexpByCategory = (props) => (

    
    <ResponsiveContainer width = '100%' height = {400} >
    <LineChart margin={{ top: 10, right: 50, left: 25, bottom: 50 }} data={props.chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="year" />
    {/* <XAxis dataKey="expense_type_id_budget"/> */}
    <YAxis 
        label={{ value: props.axisLabel, angle: -90, position: 'left' }}
        
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          }/>
    {/* <YAxis 
        label={{ value: props.axisLabel, angle: -90, position: 'left' }}
        dataKey={"capexp"}
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          }/> */}
  
            <Tooltip content={<CustomTooltip />} />
    <Legend />
    <Line dataKey="vehicle_operations" name="Vehicle Operations" stroke="black" fill="Black" />

    <Line dataKey="vehicle_maintenance" name="Vehicle Maintenance" stroke="red" fill="Red" />
    <Line dataKey="non_vehicle_maintenance" name="Non-Vehicle Maintenance" stroke="green" fill="Green" />
    <Line dataKey="general_administration" name="General Administration" stroke="blue" fill="blue" />
  </LineChart>
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