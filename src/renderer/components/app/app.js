import React, { useState, useContext, useEffect, createContext } from 'react';
import io from 'socket.io-client';

import { TabbedView, Tab } from '../tabbedview/tabbedview';
import { WelcomeComponent } from '../tabbedview/welcomecomponent';
import { to_unix_path } from '../../util/pathutils';

import './app.scss';

export const SocketContext = createContext();

function MainView() {
    const [measurements, setMeasurements] = useState([]);
    const socket = useContext(SocketContext);

    useEffect(() => {
        socket.on('measurements created', m => {
            setMeasurements([...measurements, m])
        });
    }, []);

    return (
        <TabbedView>
            <Tab path='/welcome' name='Welcome'><WelcomeComponent /></Tab>
            {
                measurements.map(m => <Tab key={m.id} name={'Wooow'} path={to_unix_path(`/file://${m.path}`)}>Hello</Tab>)
            }
        </TabbedView>
    );
}

export function App() {
    return (
        <SocketContext.Provider value={io()}>
            <MainView />
        </SocketContext.Provider>
    );
}
