import React, { useState, useEffect, createContext } from 'react';
import './app.scss';

import { TabbedView } from '../tabbedview';
import { MeasurementView } from '../measurementview';

import { WebSocketContext } from '../../websocket';

function App() {
    const [tabs, setTabs] = useState([]);

    useEffect(() => {
        if (tabs.length === 0) {
            setTabs([{ path: '/new', name: 'New' }])
        }
    }, [tabs]);

    return (
        <WebSocketContext.Provider>
            <TabbedView>
                {
                    tabs.map(tab => (
                        <MeasurementView key={tab.path} path={tab.path} name={tab.name} />
                    ))
                }
            </TabbedView>
        </WebSocketContext.Provider>

    );
}

export default App;
