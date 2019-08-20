import React, { useState, useEffect, useRef } from 'react';

import './measurementview.scss';

export function MeasurementView({path}) {
    const [websocket, setWebsocket] = useState();
    const [figure, setFigure] = useState();
    const figureElement = useRef();

    useEffect(() => {
        const websocket_type = mpl.get_websocket_type();
        setWebsocket(new websocket_type('ws://localhost:8888'));
    }, []);

    useEffect(() => {
        if (!websocket) {
            return;
        }

        websocket.onopen = () => {
            websocket.send(JSON.stringify({
                type: 'open_file',
                value: path
            }))
        }

        websocket.onmessage = ({data}) => {
            const message = JSON.parse(data)
            if (message['type'] === 'open_file_success' && message['value'] === path) {
                setFigure(new mpl.figure(parseInt(message['figure_id']), websocket, () => {}, figureElement.current))
            }
        }
    }, [websocket]);

    return (
        <div className='figure' ref={figureElement}></div>
    );
}
