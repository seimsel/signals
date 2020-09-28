import React, { useRef } from 'react';
import { useQueryParams } from '../../common/hooks/use-query-params';
import { useSize } from '../../common/hooks/use-size';

export function Figure() {
    const params = useQueryParams();
    const imgRef = useRef();
    const { width, height } = useSize(imgRef, 100);
    const queryParams = Object.entries({
        width,
        height,
        url: encodeURIComponent(params.get('url'))
    }).map(([key, value]) => `${key}=${value}`).join('&');

    let src = '';

    if (width && height) {
        src = `${process.env.SERVER_HTTP_URL}/figure?${queryParams}`;
    }

    return (
        <img
            ref={ imgRef }
            style={{
                width: '100%',
                height: '100%'
            }}
            src={ src }
        />
    );
}
