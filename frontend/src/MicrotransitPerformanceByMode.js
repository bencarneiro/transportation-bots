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

          {payload[0].payload.dr > 0 && (
            <p className="label">{`Demand Repsone: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.dr)}`}</p>
          )}
  
          {payload[0].payload.dt > 0 && (
            <p className="label">{`Taxi: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.dt)}`}</p>
          )}
          {payload[0].payload.vp > 0 && (
            <p className="label">{`Vanpool: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.vp)}`}</p>
          )}
          {payload[0].payload.jt > 0 && (
            <p className="label">{`Jitney: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.jt)}`}</p>
          )}
        </div>
      );
    }
  };
  
const MicrotransitPerformanceByMode = ({ chartData }) => (


  <ResponsiveContainer width='100%' height={400} >
    <LineChart margin={{ top: 10, right: 50, left: 25, bottom: 50 }} data={chartData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="year" />
      {/* <XAxis dataKey="expense_type_id_budget"/> */}
      <YAxis 
        tickFormatter={(value) =>
          new Intl.NumberFormat("en-US", {
            notation: "compact",
            compactDisplay: "short",
          }).format(value)
        } />
      {/* <YAxis dataKey={"capexp"}
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          }/> */}

      <Tooltip content={<CustomTooltip />} />
      <Legend />
      <Line dataKey="dr" name="Demand Response" fill="Black" stroke="Black" />

      <Line dataKey="dt" name="Taxi" fill="Red" stroke="Red" />
      <Line dataKey="vp" name="VanPool" fill="Green" stroke="Green" />
      <Line dataKey="jt" name="Jitney" fill="blue" stroke="blue" />
      {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
      {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
      {/* <Bar dataKey="year" fill="#82ca9d" /> */}
    </LineChart>
  </ResponsiveContainer>
)

MicrotransitPerformanceByMode.propTypes = {
  chartData: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number,
      expense: PropTypes.number
    })
  ).isRequired
}

export default MicrotransitPerformanceByMode