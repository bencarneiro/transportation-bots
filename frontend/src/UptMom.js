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
          
          {payload[0].payload.change_from_baseline > 0 && (
            <p className="label">{`${new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(payload[0].payload.change_from_baseline * 100)}% of ${payload[0].payload.month} 2019 ridership`}</p>
          )}
        </div>
      );
    }
  };

const UptMom = (props) => (

    
    <ResponsiveContainer width = '100%' height = {400} >
    <LineChart margin={{ top: 10, right: 50, left: 25, bottom: 50 }} data={props.chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="year"  interval={3}  />
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
    <Line dataKey="change_from_baseline" name="% of Pre-Pandemic Ridership" fill="Black" stroke="Black" />
    <Line dataKey="baseline" name="Baseline" strokeDasharray={"5 5"} stroke="Black" />

  </LineChart>
  </ResponsiveContainer>
)

UptMom.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        upt: PropTypes.number
      })
    ).isRequired
  }

export default UptMom