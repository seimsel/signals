import React, { useRef, useLayoutEffect, useEffect } from 'react';
import gql from 'graphql-tag';
import { useParams } from 'react-router';
import { useSubscription } from '@apollo/client';

const FIGURE_SUBSCRIPTION = gql`
    subscription TestSubscription($instrumentAddress: String!) {
        waveform(instrumentAddress: $instrumentAddress) {
            figure
        }
    }
`;

export function Figure() {
    const { instrumentAddress } = useParams();
    const { data } = useSubscription(FIGURE_SUBSCRIPTION, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.')
        }
    });

    const url = useRef();

    const figure = data ? data.waveform.figure : '';

    useEffect(() => {
        URL.createObjectURL(atob(figure));
    }, [figure]);

    return (
        <img
            style={{ width: '100%', height: '100%' }}
            src={url.current}
        />
    );
}
