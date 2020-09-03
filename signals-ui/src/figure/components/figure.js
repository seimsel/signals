import React from 'react';

export function Figure() {
    return (
        <img
            style={{
                width: '100%',
                height: '100%'
            }}
            src={ `${process.env.SERVER_HTTP_URL}/figure` }
        />
    );
}
