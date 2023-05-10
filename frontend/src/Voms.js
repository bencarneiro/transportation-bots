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
          {payload[0].payload.voms > 0 && (
            <p className="label">{`Vehicles Operated in Maximum Service: ${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.voms)}`}</p>
          )}
        </div>
      );
    }
  };

const Voms = (props) => (

    
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
    <Line dataKey="voms" name="Vehicles Operated in Maximum Service" fill="Black" stroke="Black" />

  </LineChart>
  </ResponsiveContainer>
)

Voms.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        voms: PropTypes.number
      })
    ).isRequired
  }

export default Voms