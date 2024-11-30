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

const VrmByService = (props) => (


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
      <Line dataKey="directly_operated" name="Directly Operated" fill="Black" stroke="Black" />

      <Line dataKey="purchased_transportation" name="Purchased Transportation" fill="Red" stroke="Red" />
      <Line dataKey="taxi" name="Taxi" fill="Green" stroke="Green" />
      <Line dataKey="other" name="Other" fill="Grey" stroke="Grey" />
      
    </LineChart>
  </ResponsiveContainer>
)

VrmByService.propTypes = {
  chartData: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number,
      upt: PropTypes.number
    })
  ).isRequired
}

export default VrmByService