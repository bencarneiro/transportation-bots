const path = require('path');

module.exports = {
  entry: './src/index.js', // Your main entry point
  output: {
    filename: 'bundle.js', // Your output file name
    path: path.resolve(__dirname, '../app/app/static/js') // Your output directory
  },
  mode: 'development', // Set to 'production' for minified output
  devtool: 'inline-source-map', // Generate source maps for debugging
  
  module: {
    rules: [
      { test: /\.css$/, use: [ 'style-loader', 'css-loader' ] },
      {
        test: /\.js$/, // Apply this rule to all .js files
        exclude: /node_modules/, // Don't apply to code from node_modules
        use: {
          loader: 'babel-loader', // Use babel-loader for transpiling
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'] // Use the env preset
          }
        }
      },
      {
        test: /\.jsx$/, // Apply this rule to all .jsx files
        exclude: /node_modules/, // Don't apply to code from node_modules
        use: {
          loader: 'babel-loader', // Use babel-loader for transpiling
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'] // Use the env and react presets
          }
        }
      }
    ]
  }
};
