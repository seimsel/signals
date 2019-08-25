const { app, BrowserWindow } = require('electron');
const { resolve } = require('path');

if (module.hot) {
    module.hot.accept();
}

app.on('ready', () => {
    const window = new BrowserWindow({
        frame: false,
        webPreferences: {
            preload: resolve(__dirname, 'preload.js')
        }
    });
    window.loadURL(`http://localhost:8080`);
});
