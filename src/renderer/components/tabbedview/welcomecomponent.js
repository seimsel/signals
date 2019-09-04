import React, { useContext } from 'react';
import { SocketContext } from '../app/app';
import { Dropzone } from './../dropzone/dropzone';

export function WelcomeComponent() {
    const socket = useContext(SocketContext);

    return (
        <Dropzone onChange={({ target }) => {
            for (let file of target.files) {
                socket.emit('measurements', 'create', {
                    path: file.path || file.name
                })
            }
        }} />
    );
}
