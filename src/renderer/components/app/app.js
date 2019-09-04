import React, { useRef, useEffect, createContext } from 'react';
import io from 'socket.io-client';

import './app.scss';

import { MeasurementView } from '../measurementview/measurementview';

export const SocketContext = createContext();

export function App() {
    return (
        <SocketContext.Provider value={io()}>
            <MeasurementView />
        </SocketContext.Provider>
    );
}
