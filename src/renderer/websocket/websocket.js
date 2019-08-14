import React, { createContext } from 'react';

export const WebSocketContext = createContext();

export const WebSocketProvider = (props) => (
    <WebSocketContext.Provider value={new WebSocket('ws://localhost:8888')}>
        {props.children}
    </WebSocketContext.Provider>
);
