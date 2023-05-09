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
          {payload[0].payload.cost_per_pmt > 0 && (
            <p className="label">{`Cost Per Passenger Mile: $${payload[0].payload.cost_per_pmt}`}</p>
          )}

        </div>
      );
    }
  };

const CostPerPmt = ({ chartData }) => (

    
    <ResponsiveContainer width = '100%' height = {400} >
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
          }/>

  
            <Tooltip content={<CustomTooltip />} />
    <Legend />
    <Line dataKey="cost_per_pmt" name="Cost Per Passenger Mile" fill="Black" stroke="Black" />

  </LineChart>
  </ResponsiveContainer>
)

CostPerPmt.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        cost_per_pmt: PropTypes.number
      })
    ).isRequired
  }

export default CostPerPmt