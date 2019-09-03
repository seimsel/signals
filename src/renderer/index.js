// import React from 'react';
// import ReactDOM from 'react-dom';
// import './index.scss';
// import { App } from './components/app/app';

import io from 'socket.io-client';

if (module.hot) {
    module.hot.accept();
}

const socket = io();
socket.on('connect', () => {
    console.log('Hello');
});

// ReactDOM.render(<App />, document.getElementById('app'));
