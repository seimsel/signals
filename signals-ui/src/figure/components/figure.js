import React from 'react';

export function Figure() {
    return (
        <img
            src={ `${process.env.SERVER_HTTP_URL}/figure` }
        />
    );
}
