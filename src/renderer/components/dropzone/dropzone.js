import React, { useContext } from 'react';

import { WebSocketContext } from '../../websocket';

import './dropzone.scss';

export function Dropzone() {
    const ws = useContext(WebSocketContext)

    console.log(ws)

    return (
        <div className='dropzone'>
            <input type='file' onChange={event => {
                ws.send(JSON.stringify(event.target.files));
            }} />
            <div>
                Drop files here or click to upload.
            </div>
        </div>
    );
}
