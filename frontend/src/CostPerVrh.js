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
          {payload[0].payload.cost_per_vrh > 0 && (
            <p className="label">{`Cost Per Vehicle Hour: $${payload[0].payload.cost_per_vrh}`}</p>
          )}

        </div>
      );
    }
  };

const CostPerVrh = ({ chartData }) => (

    
    <ResponsiveContainer width = '90%' height = {300} >
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
          }/>

  
            <Tooltip content={<CustomTooltip />} />
    <Legend />
    <Line dataKey="cost_per_vrh" name="Cost Per Vehicle Hour" fill="Black" stroke="Black" />

  </LineChart>
  </ResponsiveContainer>
)

CostPerVrh.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        cost_per_vrh: PropTypes.number
      })
    ).isRequired
  }

export default CostPerVrh