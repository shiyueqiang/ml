const os = require('os')
const path = require('path')
const webpack = require('webpack')
const autoprefixer = require('autoprefixer')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const { VueLoaderPlugin } = require('vue-loader')
let getIp = () => {
    var interfaces = require('os').networkInterfaces();
    for (var devName in interfaces) {
        var iface = interfaces[devName];
        for (var i = 0; i < iface.length; i++) {
            var alias = iface[i];
            if (alias.family === 'IPv4' && alias.address !== '127.0.0.1' && !alias.internal) {
                return alias.address;
            }
        }
    }
}

module.exports = {
    entry: {
        index: './src/main.js',
    },
    output: {
        path: path.resolve(__dirname, './html/static'),
        publicPath: '/static/',
        filename: '[name].js',
        chunkFilename: '_[name]-[chunkhash:4].js'
    },
    plugins: [new HtmlWebpackPlugin({
            filename: '../../html/index.html',
            template: path.resolve(__dirname, './src/libs/template.ejs'),
            hash: true,
            minify: {
                //清除属性引号
                removeAttributeQuotes: true,
                //清除多余空格
                collapseWhitespace: true,
                //压缩javascript
                minifyJS: true
            },
            path: '/static/',
            title: '',
            //chunks: ['index']
        }), new webpack.DllReferencePlugin({
            // name参数和dllplugin里面name一致，可以不传
            name: 'vendor',
            // dllplugin 打包输出的manifest.json
            manifest: require('./html/static/vendor.manifest.json'),
            // 和dllplugin里面的context一致
            context: path.join(__dirname, '..')
        }),
        new VueLoaderPlugin()

    ],
    module: {
        rules: [{
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    cssModules: {
                        localIdentName: 'JD_[hash:5]',
                        camelCase: true
                    },
                    postcss: [
                        autoprefixer({
                            browsers: ['last 2 versions', 'Android >= 4.0']
                        })
                    ]
                }
            },
            {
                test: /\.(less|css)$/,
                use: ['vue-style-loader', 'css-loader', {
                    loader: 'less-loader',
                    options: {
                        javascriptEnabled: true
                    }
                }]
            },
            {
                test: /\.(gif|jpg|png|woff|svg|eot|ttf)\??.*$/,
                loader: 'url-loader',
                options: {
                    name: '[hash:10].[ext]',
                    limit: 4096
                }
            }, {
                test: /\.pug$/,
                loader: 'pug-plain-loader'
            }, {
                test: /\.js?$/,
                loader: 'babel-loader',
                exclude: file => (
                    /node_modules/.test(file) &&
                    !/\.vue\.js/.test(file)
                )
            }, {
                enforce: 'pre',
                test: /\.(js|vue)$/,
                loader: 'eslint-loader',
                exclude: /node_modules/,
                options: {
                    formatter: require('eslint-friendly-formatter')//错误输出格式
                }
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    devServer: {
        contentBase: './html/',
        historyApiFallback: true,
        overlay: { warnings: false, errors: true },
        inline: true,
        hot: true,
        noInfo: true,
        host: getIp(),
        port: 3001,
        proxy: [{
            context: ['/v3', '/v2', '/xw', '/wap', '/wechat'],
            target: 'http://bm.jindanlicai.com:8463/',
            changeOrigin: true,
            cookieDomainRewrite: {
                "*": getIp()
            }
        }]
    },
    performance: {
        hints: false
    }
}


if (process.env.NODE_ENV === 'production') {
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.minimize({
            compress: {
                warnings: false
            }
        })
    ])
    module.exports.plugins.unshift(new CleanWebpackPlugin([
        path.resolve(__dirname, './html/static')
    ], {
        exclude: ['vendor.dll.js', 'vendor.manifest.json'],
        verbose: true,
        dry: false
    }))
} else {
    module.exports.devtool = '#source-map'
}