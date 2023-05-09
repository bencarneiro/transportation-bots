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

const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="custom-tooltip">
        <p className="label">{`${payload[1]}`}</p>
        <p className="mode">{`Mode: ${label}`}</p>
        <p className='expense'>{`${payload[0]}`}</p>
          {/* <p className="label">{`${active} : ${payload[0]} ${payload[1].value}}`}</p> */}
          <p className="intro">{(label)}</p>
          <p className="desc">Anything you want can be displayed here.</p>
        </div>
      );
    }
  
    return null;
  };

const BarChartComponent = ({ chartData }) => (
    <ResponsiveContainer width = '100%' height = {400} >
    <BarChart data={chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="year" />
    {/* <XAxis dataKey="" /> */}
    <YAxis dataKey={"mode_id__type"}/>
    
    <YAxis dataKey={'upt'}
          tickFormatter={(value) =>
            new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)
          } />
          
    {/* <Tooltip formatter={(value) => new Intl.NumberFormat("en-US", {
              notation: "compact",
              compactDisplay: "short",
            }).format(value)}/> */}
            <Tooltip content={<CustomTooltip />} />
    <Legend />
    <Bar dataKey="expense" name="2022 Dollars" fill="#8884d8" />
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