const { app, BrowserWindow } = require('electron');

if (module.hot) {
    module.hot.accept();
}

app.on('ready', () => {
    const window = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true
        }
    });
    window.loadURL(`http://localhost:8080`);
});
