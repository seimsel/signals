import React, { useEffect, useState } from 'react';
import { QtContext } from '../contexts/qt-context';

export function QtProvider({ children }) {
    const [python, setPython] = useState();

    useEffect(() => {
        if (!window.qt) {
            return;
        }

        (async () => {
            const { QWebChannel } = await import('qwebchannel');

            new QWebChannel(
                qt.webChannelTransport,
                channel => {
                    setPython(channel.objects.python);
                }
            );
        })();

    }, []);

    return (
        <QtContext.Provider value={python}>
            {children}
        </QtContext.Provider >
    );
}
