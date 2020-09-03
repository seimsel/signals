import React, { useRef } from 'react';
import { useSize } from '../../common/hooks/use-size';

export function Figure() {
    const imgRef = useRef();
    const { width, height } = useSize(imgRef, 100);

    return (
        <img
            ref={ imgRef }
            style={{
                width: '100%',
                height: '100%'
            }}
            src={ `${process.env.SERVER_HTTP_URL}/figure?width=${width}&height=${height}` }
        />
    );
}
