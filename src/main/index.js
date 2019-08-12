import { app, BrowserWindow } from 'electron';
import { startBackend } from './backend';

if (module.hot) {
    module.hot.accept();
}

app.on('ready', () => {
    const window = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true
        }
    });
    startBackend();
    window.loadURL(`http://localhost:${process.env.ELECTRON_WEBPACK_WDS_PORT}`);
});
