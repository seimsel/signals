const { app, BrowserWindow } = require('electron');
const { resolve } = require('path');
const { findPorts } = require('./util/networkutils');
const { spawn } = require('child_process');

const { findPython } = require('./util/pythonutils');

app.on('ready', () => {
    findPython(['python', 'python3'], (python) => {
        findPorts(3000, 5000, 1, ([port]) => {
            const backend = spawn('nodemon', ['--exec', python, 'src/backend/main.py', `--port=${port}`], {
                shell: true
            });
            backend.stdout.on('data', data => console.log(`${data}`));
            backend.stderr.on('data', data => console.error(`${data}`));

            const frontend = spawn('webpack', ['--config', 'webpack.renderer.config.js', '--watch'], {
                shell: true
            });
            frontend.stdout.on('data', data => console.log(`${data}`));
            frontend.stderr.on('data', data => console.error(`${data}`));

            const window = new BrowserWindow({
                frame: false,
                backgroundColor: '#1e1e1e',
                webPreferences: {
                    preload: resolve(__dirname, 'preload.js')
                }
            });
            
            window.loadURL(`http://localhost:${port}`);

            app.on('before-quit', () => {
                frontend.kill();
                backend.kill();
            })
        });
    });
});
