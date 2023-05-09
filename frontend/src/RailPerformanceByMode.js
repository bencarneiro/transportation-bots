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
          {payload[0].payload.mb > 0 && (
            <p className="label">{`City Bus: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.mb)}`}</p>
          )}
  
          {payload[0].payload.hr > 0 && (
            <p className="label">{`Heavy Rail: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.hr)}`}</p>
          )}
          {payload[0].payload.lr > 0 && (
            <p className="label">{`Light Rail: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.lr)}`}</p>
          )}
          {payload[0].payload.cr > 0 && (
            <p className="label">{`Commuter Rail: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.cr)}`}</p>
          )}
          {payload[0].payload.yr > 0 && (
            <p className="label">{`Hybrid Rail: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.yr)}`}</p>
          )}
          {payload[0].payload.sr > 0 && (
            <p className="label">{`Street Car: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.sr)}`}</p>
          )}
          {payload[0].payload.cc > 0 && (
            <p className="label">{`Cable Car: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.cc)}`}</p>
          )}
          {payload[0].payload.mg > 0 && (
            <p className="label">{`Monorail: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.mg)}`}</p>
          )}
          {payload[0].payload.ip > 0 && (
            <p className="label">{`Inclined Plane: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.ip)}`}</p>
          )}
          {payload[0].payload.ar > 0 && (
            <p className="label">{`Alaskan Railway:${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.ar)}`}</p>
          )}
        </div>
      );
    }
  };
  
const RailPerformanceByMode = ({ chartData }) => (


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
      <Line dataKey="hr" name="Heavy Rail" fill="Black" stroke="Black" />
      <Line dataKey="lr" name="Light Rail" fill="Red" stroke="Red" />
      <Line dataKey="cr" name="Commuter Rail" fill="Green" stroke="Green" />
      <Line dataKey="sr" name="Street Rail" fill="blue" stroke="blue" />
      <Line dataKey="yr" name="Hybrid Rail" fill="Orange" stroke="Orange" />
      <Line dataKey="cc" name="Cable Car" fill="Purple" stroke="Purple" />
      <Line dataKey="mg" name="MonoRail" fill="Grey" stroke="Grey" />
      <Line dataKey="ip" name="Inclined Plane" fill="cyan" stroke="cyan" />
      <Line dataKey="cc" name="Cable Car" fill="magenta" stroke="magenta" />
      <Line dataKey="ar" name="Alaska Rail" fill="black" stroke="black" />

      <Line dataKey="or" name="Other" fill="black" stroke="black" />
      {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
      {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
      {/* <Bar dataKey="year" fill="#82ca9d" /> */}
    </LineChart>
  </ResponsiveContainer>
)

RailPerformanceByMode.propTypes = {
  chartData: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number,
      expense: PropTypes.number
    })
  ).isRequired
}

export default RailPerformanceByMode