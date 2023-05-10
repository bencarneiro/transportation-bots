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
        <p className="label">{`Rolling Stock: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.rolling_stock)}`}</p>
        <p className="label">{`Facilities: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.facilities)}`}</p>
        <p className="label">{`Other Capital: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.other_capital)}`}</p>
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

const CapexpByCategory = (props) => (

    
    <ResponsiveContainer width = '100%' height = {400} >
    <LineChart margin={{ top: 10, right: 50, left: 25, bottom: 50 }} data={props.chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="year" />
    {/* <XAxis dataKey="expense_type_id_budget"/> */}
    <YAxis label={{ value: props.axisLabel, angle: -90, position: 'left' }}
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
    <Line dataKey="rolling_stock" name="Rolling Stock" stroke="black" fill="black" />

    <Line dataKey="facilities" name="Facilities" stroke="red" fill="red" />
    <Line dataKey="other_capital" name="Other Capital" stroke="blue" fill="blue" />
    {/* <Bar dataKey="general_administration" name="General Administration" fill="Grey" /> */}
    {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
    {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
    {/* <Bar dataKey="year" fill="#82ca9d" /> */}
  </LineChart>
  </ResponsiveContainer>
)

CapexpByCategory.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        expense: PropTypes.number
      })
    ).isRequired
  }

export default CapexpByCategory