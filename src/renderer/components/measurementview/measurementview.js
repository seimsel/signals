import React, { useState, useEffect, useContext } from 'react';

import { SocketContext } from '../app/app';

export function MeasurementView({ location }) {
    const socket = useContext(SocketContext);

    useEffect(() => {
        socket.on('connect', () => {
            // socket.emit('clients', 'create', (client) => {
            //     console.log(client);
            // });
        })
    }, [socket])

    return null;
}
