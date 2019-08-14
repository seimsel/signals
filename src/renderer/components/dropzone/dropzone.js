import React, { useContext } from 'react';

import { WebSocketContext } from '../../websocket';

import './dropzone.scss';

export function Dropzone() {
    const ws = useContext(WebSocketContext)

    return (
        <div className='dropzone'>
            <input type='file' multiple onChange={event => {
                for (let file of event.target.files) {
                    ws.send(JSON.stringify({
                        type: 'open_file',
                        value: { 
                            path: file.path || file.name
                        }
                    }));
                }
            }} />
            <div>
                Drop files here or click to upload.
            </div>
        </div>
    );
}
