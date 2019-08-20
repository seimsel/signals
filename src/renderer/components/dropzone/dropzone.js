import React from 'react';

import './dropzone.scss';

export function Dropzone({onChange}) {
    return (
        <div className='dropzone'>
            <input type='file' multiple onChange={onChange} />
            <div>
                Drop files here or click to upload.
            </div>
        </div>
    );
}
