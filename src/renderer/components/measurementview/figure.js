import React, { useLayoutEffect, useRef } from 'react';

import './figure.scss';

export function Figure({ id }) {
    const canvasRef = useRef();
    const resizeTimerRef = useRef();
    const websocketRef = useRef();
    const imageRef = useRef();

    useLayoutEffect(() => {
        if (!id) {
            return;
        }

        if (!imageRef.current) {
            imageRef.current = new Image();
        }

        if (!websocketRef.current) {
            websocketRef.current = new WebSocket(`ws://localhost:${window.backendPort}/matplotlib`);
        }

        websocketRef.current.onopen = () => {
            window.onresize = () => {
                if (resizeTimerRef) {
                    clearTimeout(resizeTimerRef.current);
                }
                resizeTimerRef.current = setTimeout(() => {
                    websocketRef.current.send(JSON.stringify({
                        type: 'resize',
                        width: canvasRef.current.offsetWidth,
                        height: canvasRef.current.offsetHeight,
                        figure_id: id
                    }));
                }, 250);
            };
    
            websocketRef.current.send(JSON.stringify({
                type: 'resize',
                width: canvasRef.current.offsetWidth,
                height: canvasRef.current.offsetHeight,
                figure_id: id
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
                    figure_id: id
                }));
            }
            else {
                const message = JSON.parse(data)

                if (message['type'] === 'refresh') {
                    websocketRef.current.send(JSON.stringify({
                        type: 'refresh',
                        figure_id: id
                    }));
                }
                else if (message['type'] === 'draw') {
                    websocketRef.current.send(JSON.stringify({
                        type: 'draw',
                        figure_id: id
                    }));
                }
                else if (message['type'] === 'resize') {
                    canvasRef.current.width = canvasRef.current.offsetWidth;
                    canvasRef.current.height = canvasRef.current.offsetHeight;
                }
            }
        }
    }, [id]);

    if (!id) {
        return null;
    }

    return (
        <canvas ref={canvasRef} className='figure'></canvas>
    );
}
