import React, { useLayoutEffect, useRef } from 'react';

import './measurementview.scss';

export function MeasurementView({ location }) {
    const canvasRef = useRef();
    const resizeTimerRef = useRef();
    const websocketRef = useRef();
    const imageRef = useRef();
    const figureIdRef = useRef();

    useLayoutEffect(() => {
        if (!imageRef.current) {
            imageRef.current = new Image();
        }

        if (!websocketRef.current) {
            websocketRef.current = new WebSocket('ws://localhost:8888');
        }

        websocketRef.current.onopen = () => {
            websocketRef.current.send(JSON.stringify({
                type: 'open_file',
                value: location.pathname.substr(1)
            }));

            window.onresize = () => {
                if (resizeTimerRef) {
                    clearTimeout(resizeTimerRef.current);
                }
                resizeTimerRef.current = setTimeout(() => {
                    websocketRef.current.send(JSON.stringify({
                        type: 'resize',
                        width: canvasRef.current.offsetWidth,
                        height: canvasRef.current.offsetHeight,
                        figure_id: figureIdRef.current
                    }));
                }, 250);
            };
    
            websocketRef.current.send(JSON.stringify({
                type: 'resize',
                width: canvasRef.current.offsetWidth,
                height: canvasRef.current.offsetHeight,
                figure_id: figureIdRef.current
            }));
        }

        websocketRef.current.onmessage = ({data}) => {
            if (data instanceof Blob) {
                if (imageRef.current.src) {
                    window.URL.revokeObjectURL(imageRef.current.src);
                }

                imageRef.current.src = window.URL.createObjectURL(data);
                imageRef.current.onload = () => {
                    canvasRef.current.getContext('2d').drawImage(imageRef.current, 0, 0);
                }
                websocketRef.current.send(JSON.stringify({
                    type: 'ack',
                    figure_id: figureIdRef.current
                }));
            }
            else {
                const message = JSON.parse(data)

                if (message['type'] === 'open_file_success' && message['value'] === location.pathname) {
                    figureIdRef.current = message['figure_id'];
                }
                else if (message['type'] === 'refresh') {
                    websocketRef.current.send(JSON.stringify({
                        type: 'refresh',
                        figure_id: figureIdRef.current
                    }));
                }
                else if (message['type'] === 'draw') {
                    websocketRef.current.send(JSON.stringify({
                        type: 'draw',
                        figure_id: figureIdRef.current
                    }));
                }
                else if (message['type'] === 'resize') {
                    canvasRef.current.width = canvasRef.current.offsetWidth;
                    canvasRef.current.height = canvasRef.current.offsetHeight;
                }
            }
        }
    }, []);

    return (
        <canvas ref={canvasRef} className='figure'></canvas>
    );
}
