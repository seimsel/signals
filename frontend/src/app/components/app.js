import React, { useRef, useLayoutEffect } from 'react';
import gql from 'graphql-tag';
import { useSubscription } from '@apollo/react-hooks';
import { ApiProvider } from '../../api/components/api-provider';

const TEST_SUBSCRIPTION = gql`
    subscription TestSubscription {
        scope(address: "10.1.11.79") {
            channels {
                waveform {
                    figure
                }
            }
        }
    }
`;

function Test() {
    const { data } = useSubscription(TEST_SUBSCRIPTION);
    const container = useRef();

    const figure = data ? data.scope.channels[0].waveform.figure : '';

    useLayoutEffect(() => {
        if (!(container.current && container.current.children[0])) {
            return;
        }
        
        container.current.children[0].setAttribute('height', '100%');
        container.current.children[0].setAttribute('width', '100%');
        container.current.children[0].setAttribute('preserveAspectRatio', 'none');
    });

    return (
        <div className='full-size' dangerouslySetInnerHTML={{ __html: figure }} ref={container} />
    );
}

export function App() {
    return (
        <ApiProvider>
            <Test />
        </ApiProvider>
    );
}
