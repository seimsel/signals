const { resolve } = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const LiveReloadPlugin = require('webpack-livereload-plugin');

module.exports = {
    mode: 'development',
    entry: './src/renderer/index.js',
    output: {
        path: resolve(__dirname, 'static'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/env', '@babel/react']
                }
            },
            {
                test: /\.scss$/,
                exclude: /node_modules/,
                loader: ['style-loader', 'css-loader', 'sass-loader']
            }
        ]
    },
    devtool: 'eval-source-map',
    target: 'web',
    stats: 'errors-warnings',
    plugins: [
        new LiveReloadPlugin(),
        new HtmlWebpackPlugin({
            template: './src/renderer/index.html'
        })
    ]
}
