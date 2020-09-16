import React, { useEffect, useState } from 'react';
import { QWebChannel } from 'qwebchannel';
import { QtContext } from '../contexts/qt-context';

export function QtProvider({ children }) {
    const [python, setPython] = useState();

    useEffect(() => {
        if (!qt) {
            return;
        }

        new QWebChannel(
            qt.webChannelTransport,
            channel => {
                setPython(channel.objects.python);
            });
    }, []);

    return (
        <QtContext.Provider value={python}>
            {children}
        </QtContext.Provider >
    );
}
