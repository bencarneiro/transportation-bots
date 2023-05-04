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
        {payload[0].payload.bus > 0 && (
          <p className="label">{`Bus: ${new Intl.NumberFormat("en-US", {
            notation: "compact",
            compactDisplay: "short",
          }).format(payload[0].payload.bus)}`}</p>
        )}

        {payload[0].payload.rail > 0 && (
          <p className="label">{`Rail: ${new Intl.NumberFormat("en-US", {
            notation: "compact",
            compactDisplay: "short",
          }).format(payload[0].payload.rail)}`}</p>
        )}
        {payload[0].payload.microtransit > 0 && (
          <p className="label">{`MicroTransit: ${new Intl.NumberFormat("en-US", {
            notation: "compact",
            compactDisplay: "short",
          }).format(payload[0].payload.microtransit)}`}</p>
        )}
        {payload[0].payload.ferry > 0 && (
          <p className="label">{`Ferry: ${new Intl.NumberFormat("en-US", {
            notation: "compact",
            compactDisplay: "short",
          }).format(payload[0].payload.ferry)}`}</p>
        )}
        {payload[0].payload.other > 0 && (
          <p className="label">{`Other: ${new Intl.NumberFormat("en-US", {
            notation: "compact",
            compactDisplay: "short",
          }).format(payload[0].payload.other)}`}</p>
        )}
      </div>
    );
  }
};

const VrhByModeType = ({ chartData }) => (


  <ResponsiveContainer width='90%' height={300} >
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
      <Line dataKey="bus" name="Bus" fill="Black" stroke="Black" />

      <Line dataKey="rail" name="Rail" fill="Red" stroke="Red" />
      <Line dataKey="microtransit" name="MicroTransit" fill="Green" stroke="Green" />
      <Line dataKey="ferry" name="Ferry" fill="blue" stroke="blue" />
      <Line dataKey="other" name="Other" fill="Grey" stroke="Grey" />
      {/* <Bar dataKey="expense_type_id_budget" name="2022 Dollars" fill="#Black" /> */}
      {/* <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" /> */}
      {/* <Bar dataKey="year" fill="#82ca9d" /> */}
    </LineChart>
  </ResponsiveContainer>
)

VrhByModeType.propTypes = {
  chartData: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number,
      voms: PropTypes.number
    })
  ).isRequired
}

export default VrhByModeType