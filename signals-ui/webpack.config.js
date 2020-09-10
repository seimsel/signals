const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');
const { DefinePlugin } = require('webpack');
const package = require('./package.json');
const dark = require('antd/dist/dark-theme');

const isDevelopment = process.env.NODE_ENV !== 'production';

function titleCase(str) {
    return (
        str.toLowerCase()
        .split(' ')
        .map(word => `${word.charAt(0).toUpperCase()}${word.slice(1)}`)
        .join(' ')
    );
}

function getPort(url) {
    const urlObj = new URL(url);
    return urlObj.port || 8080;
}

module.exports = {
    mode: isDevelopment ? 'development' : 'production',
    entry: './src/index.js',
    devtool: isDevelopment && 'source-map',

    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: '/'
    },

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: [
                    {
                        loader: 'babel-loader',
                        options: {
                            presets: [
                                '@babel/preset-env',
                                '@babel/preset-react'
                            ],
                            plugins: [
                                ['import', {
                                    libraryName: 'antd',
                                    style: true
                                }],
                                isDevelopment && 'react-refresh/babel'
                            ].filter(Boolean),
                        }
                    }
                ]
            },
            {
                test: /.less$/,
                exclude: /src/,
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader"
                }, {
                    loader: "less-loader",
                    options: {
                        lessOptions: {
                            modifyVars: dark,
                            javascriptEnabled: true
                        }
                    }
                }]
            },
            {
                test: /\.less$/,
                exclude: /node_modules/,
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader"
                }, {
                    loader: "less-loader"
                }]
            },
            {
                test: /\.(graphql)$/,
                exclude: /node_modules/,
                loader: 'graphql-tag/loader',
            },
        ]
    },

    plugins: [
        new DefinePlugin({
            'process.env.SERVER_HTTP_URL': JSON.stringify(process.env.SERVER_HTTP_URL),
            'process.env.SERVER_WS_URL': JSON.stringify(process.env.SERVER_WS_URL)
        }),
        new HtmlWebpackPlugin({
            title: `${titleCase(package.name)} ${package.version}`,
            template: './src/index.html'
        }),
        isDevelopment && new ReactRefreshWebpackPlugin()
    ].filter(Boolean),

    devServer: {
        historyApiFallback: true,
        hot: true,
        port: getPort(process.env.UI_HTTP_URL)
    }
};
