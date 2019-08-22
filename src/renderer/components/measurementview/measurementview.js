import React, { useState, useEffect, useRef } from 'react';

import './measurementview.scss';

export function MeasurementView({path}) {
    const canvasRef = useRef();
    const resizeTimerRef = useRef();
    const [websocket, setWebsocket] = useState();
    const [image, setImage] = useState();
    const [figureId, setFigureId] = useState();

    useEffect(() => {
        setWebsocket(new WebSocket('ws://localhost:8888'));
        setImage(new Image());
    }, []);

    useEffect(() => {
        if (!websocket) {
            return;
        }

        websocket.onopen = () => {
            websocket.send(JSON.stringify({
                type: 'open_file',
                value: path
            }));

            window.onresize = () => {
                if (resizeTimerRef) {
                    clearTimeout(resizeTimerRef.current);
                }
                resizeTimerRef.current = setTimeout(() => {
                    websocket.send(JSON.stringify({
                        type: 'resize',
                        width: canvasRef.current.offsetWidth,
                        height: canvasRef.current.offsetHeight,
                        figure_id: figureId
                    }));
                }, 250);
            };
    
            window.onresize();
        }

        websocket.onmessage = ({data}) => {
            if (data instanceof Blob) {
                if (image.src) {
                    window.URL.revokeObjectURL(image.src);
                }

                image.src = window.URL.createObjectURL(data);
                image.onload = () => {
                    canvasRef.current.getContext('2d').drawImage(image, 0, 0);
                }
                websocket.send(JSON.stringify({
                    type: 'ack',
                    figure_id: figureId
                }));
            }
            else {
                const message = JSON.parse(data)

                if (message['type'] === 'open_file_success' && message['value'] === path) {
                    setFigureId(message['figure_id']);
                }
                else if (message['type'] === 'refresh') {
                    websocket.send(JSON.stringify({
                        type: 'refresh',
                        figure_id: figureId
                    }));
                }
                else if (message['type'] === 'draw') {
                    websocket.send(JSON.stringify({
                        type: 'draw',
                        figure_id: figureId
                    }));
                }
                else if (message['type'] === 'resize') {
                    canvasRef.current.width = canvasRef.current.offsetWidth;
                    canvasRef.current.height = canvasRef.current.offsetHeight;
                }
            }
        }
    }, [websocket]);

    return (
        <canvas ref={canvasRef} className='figure'></canvas>
    );
}
