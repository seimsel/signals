const { app, BrowserWindow } = require('electron');
const { resolve } = require('path');
const { findPorts } = require('./util/networkutils');
const { spawn } = require('child_process');

const { findPython } = require('./util/pythonutils');

if (module.hot) {
    module.hot.accept();
}

app.on('ready', () => {
    findPython(['python', 'python3'], (python) => {
        findPorts(3000, 5000, 2, ([backendPort, frontendPort]) => {
            const backend = spawn('nodemon', ['--exec', python, 'src/backend/main.py', '--port', `${backendPort}`], {
                shell: true
            });
            backend.stdout.on('data', data => console.log(`${data}`));
            backend.stderr.on('data', data => console.error(`${data}`));

            const frontend = spawn('webpack-dev-server', ['--config', 'webpack.renderer.config.js', '--port', `${frontendPort}`], {
                shell: true
            });
            frontend.stdout.on('data', data => console.log(`${data}`));
            frontend.stderr.on('data', data => console.error(`${data}`));

            process.env.backendPort = backendPort;

            const window = new BrowserWindow({
                frame: false,
                backgroundColor: '#1e1e1e',
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


});
