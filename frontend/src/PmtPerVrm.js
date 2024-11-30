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
          {payload[0].payload.pmt_per_vrm > 0 && (
            <p className="label">{`Passenger Miles per Vehicle Mile: ${payload[0].payload.pmt_per_vrm}`}</p>
          )}

        </div>
      );
    }
  };

const PmtPerVrm = (props) => (

    
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
    <Line dataKey="pmt_per_vrm" name="Pass. Miles / Veh. Mile" fill="Black" stroke="Black" />

    {/* <Line dataKey="purchased_transportation" name="Purchased Transportation" fill="Red" stroke="Red"/>
    <Line dataKey="taxi" name="Taxi" fill="Taxi" stroke="Green" />
    <Line dataKey="other" name="Other" fill="Other" stroke="Orange" /> */}
    
  </LineChart>
  </ResponsiveContainer>
)

PmtPerVrm.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        pmt_per_vrm: PropTypes.number
      })
    ).isRequired
  }

export default PmtPerVrm