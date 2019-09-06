import React, { useState, useRef, useContext, useEffect, createContext } from 'react';
import io from 'socket.io-client';

import { TabbedView, Tab } from '../tabbedview/tabbedview';
import { WelcomeComponent } from '../tabbedview/welcomecomponent';
import { to_unix_path } from '../../util/pathutils';

import './app.scss';

export const SocketContext = createContext();

function useListener(eventName, callback, dependencies) {
    const socket = useContext(SocketContext);
    const oldListener = useRef();

    useEffect(() => {
        if (oldListener.current) {
            socket.removeListener(oldListener);
        }
    
        socket.on(eventName, callback);
        oldListener.current = callback;
    }, dependencies);
}

function MainView() {
    const [measurements, setMeasurements] = useState([]);

    useListener('measurements created', m => {
        setMeasurements([...measurements, m]);
    }, [measurements]);

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
