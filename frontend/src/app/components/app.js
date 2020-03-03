import React, { useRef } from 'react';
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
    const figure = data ? data.scope.channels[0].waveform.figure : '';

    return (
        <div style={{
            width: '100%'
        }} dangerouslySetInnerHTML={{ __html: figure }} />
    );
}

export function App() {
    return (
        <ApiProvider>
            <Test />
        </ApiProvider>
    );
}
