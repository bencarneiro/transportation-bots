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
} from 'recharts'

const moment = require('moment')

const BarChartComponent = ({ chartData }) => (
    <ResponsiveContainer width = '90%' height = {300} >
    <BarChart width={730} height={250} data={chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="year" />
    <YAxis
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          } />
    <Tooltip />
    <Legend />
    <Bar dataKey="expense" fill="#8884d8" />
    <Bar dataKey="year" fill="#82ca9d" />
  </BarChart>
  </ResponsiveContainer>
)

BarChartComponent.propTypes = {
    chartData: PropTypes.arrayOf(
      PropTypes.shape({
        year: PropTypes.number,
        expense: PropTypes.number
      })
    ).isRequired
  }

export default BarChartComponent