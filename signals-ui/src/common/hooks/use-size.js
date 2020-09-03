import React, { useEffect, useState } from 'react';
import { useDebounce } from './use-debounce';

export function useSize(imgRef, debounce=0) {
    const [size, setSize] = useState({
        width: undefined,
        height: undefined
    });

    const debouncedSize = useDebounce(size, debounce);

    function onResize() {
        setSize({
            width: imgRef.current.offsetWidth,
            height: imgRef.current.offsetHeight,
        });
    }

    useEffect(() => {
        const resizeListener = window.addEventListener('resize', onResize);
        onResize();

        return () => {
            window.removeEventListener('resize', resizeListener);
        }
    }, []);
  
    return {
        width: debouncedSize.width || size.width,
        height: debouncedSize.height || size.height
    };
}
