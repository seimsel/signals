import React, { useRef, useEffect, createContext } from 'react';
import './app.scss'; 

import { TabbedView } from '../tabbedview/tabbedview';
import { MainComponent } from '../tabbedview/maincomponent';

export const WebsocketContext = createContext();

export function App() {
    return (
        <WebsocketContext.Provider value={new WebSocket(`ws://localhost:${window.backendPort}`)}>
            <TabbedView mainComponent={MainComponent} />
        </WebsocketContext.Provider>
    );
}
