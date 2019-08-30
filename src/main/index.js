const { app, BrowserWindow } = require('electron');
const { resolve } = require('path');
const { findPorts } = require('./util/networkutils');
const { spawn } = require('child_process');

if (module.hot) {
    module.hot.accept();
}


app.on('ready', () => {
    findPorts(3000, 5000, 2, ([backendPort, frontendPort]) => {
        const backend = spawn('cmd', ['/C', 'nodemon', 'src/backend/main.py', '--port', `${backendPort}`]);
        backend.stdout.on('data', data => console.log(`${data}`));
        backend.stderr.on('data', data => console.error(`${data}`));

        const frontend = spawn('cmd', ['/C', 'webpack-dev-server', '--config', 'webpack.renderer.config.js', '--port', `${frontendPort}`]);
        frontend.stdout.on('data', data => console.log(`${data}`));
        frontend.stderr.on('data', data => console.error(`${data}`));

        process.env.backendPort = backendPort;

        const window = new BrowserWindow({
            frame: false,
            webPreferences: {
                preload: resolve(__dirname, 'preload.js')
            }
        });
        
        window.loadURL(`http://localhost:${frontendPort}`);

        app.on('before-quit', () => {
            frontend.kill();
            backend.kill();
        })
    });
});
