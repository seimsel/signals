import React, { useEffect, useState } from 'react';
import { useDebounce } from './use-debounce';

export function useSize(elementRef, debounce=0) {
    const [size, setSize] = useState({
        width: undefined,
        height: undefined
    });

    const debouncedSize = useDebounce(size, debounce);

    function onResize() {
        setSize({
            width: elementRef.current.offsetWidth,
            height: elementRef.current.offsetHeight,
        });
    }

    useEffect(() => {
        const resizeObserver = new ResizeObserver(entries => {
            onResize();
        });
        onResize();

        resizeObserver.observe(elementRef.current);

        return () => {
            resizeObserver.disconnect();
        }
    }, []);
  
    return {
        width: debouncedSize.width || size.width,
        height: debouncedSize.height || size.height
    };
}
