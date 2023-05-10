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
  
          {payload[0].payload.rb > 0 && (
            <p className="label">{`Rapid Bus: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.rb)}`}</p>
          )}
          {payload[0].payload.cb > 0 && (
            <p className="label">{`Commuter Bus: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.cb)}`}</p>
          )}
          {payload[0].payload.tb > 0 && (
            <p className="label">{`Trolley Bus: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.tb)}`}</p>
          )}
          {payload[0].payload.pb > 0 && (
            <p className="label">{`Other:${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.pb)}`}</p>
          )}
        </div>
      );
    }
  };
  
const BusPerformanceByMode = (props) => (


  <ResponsiveContainer width='100%' height={400} >
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
        } />
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
      <Line dataKey="mb" name="City Bus" fill="Black" stroke="Black" />

      <Line dataKey="rb" name="Rapid Bus" fill="Red" stroke="Red" />
      <Line dataKey="tb" name="Trolley Bus" fill="Green" stroke="Green" />
      <Line dataKey="cb" name="Commuter Bus" fill="b,ue" stroke="blue" />
      <Line dataKey="pb" name="Publico" fill="Grey" stroke="Grey" />
      {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
      {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
      {/* <Bar dataKey="year" fill="#82ca9d" /> */}
    </LineChart>
  </ResponsiveContainer>
)

BusPerformanceByMode.propTypes = {
  chartData: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number,
      expense: PropTypes.number
    })
  ).isRequired
}

export default BusPerformanceByMode