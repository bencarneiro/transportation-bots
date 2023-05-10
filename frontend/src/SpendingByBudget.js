import React from 'react'
import PropTypes from 'prop-types'
// import moment from 'moment'


import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
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
        <p className="label">{`Operating Expenses: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.opexp)}`}</p>
        <p className="label">{`Capital Expenses: ${new Intl.NumberFormat("en-US", {
        notation: "compact",
        compactDisplay: "short",
      }).format(payload[0].payload.capexp)}`}</p>
        </div>
      );
    }
  };

const SpendingByBudget = (props) => (

    
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

            <Tooltip content={<CustomTooltip />} />
    <Legend />
    <Line dataKey="opexp" name="Operating Expenditures" stroke="black" fill="black" />

    <Line dataKey="capexp" name="Capital Expenditures" stroke="red" fill="Red" />
    {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
    {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
    {/* <Bar dataKey="year" fill="#82ca9d" /> */}
  </LineChart>
  </ResponsiveContainer>
)

SpendingByBudget.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        expense: PropTypes.number
      })
    ).isRequired
  }

export default SpendingByBudget