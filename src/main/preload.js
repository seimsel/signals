const { remote } = require('electron');

window.isMaximized = () => remote.getCurrentWindow().isMaximized();
window.maximize = () => remote.getCurrentWindow().maximize();
window.restore = () => remote.getCurrentWindow().restore();
window.minimize = () => remote.getCurrentWindow().minimize();
window.backendPort = process.env.backendPort;
