import React from 'react'
import PropTypes from 'prop-types'
// import moment from 'moment'


import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const moment = require('moment')

const TimeSeriesChart = ({ chartData }) => (
  <ResponsiveContainer width = '90%' height = {500} >
    <ScatterChart>
      <XAxis
        dataKey = 'year'
        domain = {['auto', 'auto']}
        name = 'Time'
        // tickFormatter = {(unixTime) => moment(unixTime).format('HH:mm Do')}
        type = 'number'
      />
      <YAxis dataKey = 'expense' 
      name = 'Value' 
      // dx={10}
      domain = {['auto', 'auto']}
      tickFormatter={(value) =>
        new Intl.NumberFormat("en-US", {
          notation: "compact",
          compactDisplay: "short",
        }).format(value)
      }
      />

      <Scatter
        data = {chartData}
        line = {{ stroke: '#eee' }}
        lineJointType = 'monotoneX'
        lineType = 'joint'
        name = 'Values'
      />

    </ScatterChart>
  </ResponsiveContainer>
)

TimeSeriesChart.propTypes = {
  chartData: PropTypes.arrayOf(
    PropTypes.shape({
      year: PropTypes.number,
      expense: PropTypes.number
    })
  ).isRequired
}

export default TimeSeriesChart