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
  Line,
  LineChart
} from 'recharts'

const moment = require('moment')

const CustomTooltip = ({ active, payload, label }) => {
    // console.log(payload)
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip" style={{ backgroundColor: "white", fontSize: "16px", margin: "10px" }}>
          <h3 className="label">{`${payload[0].payload.year}`}</h3>
          {payload[0].payload.frr > 0 && (
            <p className="label">{`Fare Recovery Ratio: ${payload[0].payload.frr}`}</p>
          )}

        </div>
      );
    }
  };

const Frr = ({ chartData }) => (

    
    <ResponsiveContainer width = '90%' height = {300} >
    <LineChart width={730} height={250} data={chartData}>
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
    <Line dataKey="frr" name="Fare Recovery Ratio" fill="Black" stroke="Black" />

    {/* <Line dataKey="purchased_transportation" name="Purchased Transportation" fill="Red" stroke="Red"/>
    <Line dataKey="taxi" name="Taxi" fill="Taxi" stroke="Green" />
    <Line dataKey="other" name="Other" fill="Other" stroke="Orange" /> */}
    {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
    {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
    {/* <Bar dataKey="year" fill="#82ca9d" /> */}
  </LineChart>
  </ResponsiveContainer>
)

Frr.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        frr: PropTypes.number
      })
    ).isRequired
  }

export default Frr