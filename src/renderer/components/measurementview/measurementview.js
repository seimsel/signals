import React, { useState, useEffect, useContext } from 'react';

import { WebsocketContext } from '../app/app';
import { Figure } from './figure';

export function MeasurementView({ location }) {
    const [figureId, setFigureId] = useState();
    const websocket = useContext(WebsocketContext);
    
    useEffect(() => {
        websocket.send(JSON.stringify({
            service: 'measurements',
            action: 'create',
            data: {
                path: location.pathname.substr(1)
            }
        }));

        websocket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message['action'] === 'created' && message['service'] === 'measurements' && message['data']['path'] === location.pathname.substr(1)) {
                setFigureId(message['data']['figure']);
            }
        };
    }, []);

    return <Figure id={figureId} />;
}
