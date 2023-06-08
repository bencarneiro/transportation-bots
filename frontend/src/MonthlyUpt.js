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
          <h3 className="label">{`${payload[0].payload.month} ${payload[0].payload.year}`}</h3>
          {payload[0].payload.upt > 0 && (
            <p className="label">{`Passengers: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.upt)}`}</p>
          )}
          {payload[0].payload.vrm > 0 && (
            <p className="label">{`Vehicle Miles: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.vrm)}`}</p>
          )}
          {payload[0].payload.vrh > 0 && (
            <p className="label">{`Vehicle Hours: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.vrh)}`}</p>
          )}
          {payload[0].payload.upt_per_vrh > 0 && (
            <p className="label">{`Passengers Per Vehicle Hour: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.upt_per_vrh)}`}</p>
          )}
        </div>
      );
    }
  };

const MonthlyUpt = (props) => (

    
    <ResponsiveContainer width = '100%' height = {400} >
    <LineChart margin={{ top: 10, right: 50, left: 25, bottom: 50 }} data={props.chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="date" 
    tickFormatter={(value) =>
        new Date(value).getFullYear()}
    />
    {/* <XAxis dataKey="expense_type_id_budget"/> */}
    <YAxis label={{ value: props.axisLabel, angle: -90, position: 'left' }}
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          }/>
  
            <Tooltip content={<CustomTooltip />} />
    <Legend />
    <Line dataKey={props.dataKey} name={props.lineLabel} fill="Black" stroke="Black" />

  </LineChart>
  </ResponsiveContainer>
)

MonthlyUpt.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        month: PropTypes.number,
        upt: PropTypes.number
      })
    ).isRequired
  }

export default MonthlyUpt