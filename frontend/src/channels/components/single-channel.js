import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useParams } from 'react-router';
import { Link } from 'react-router-dom';
import { ParameterList } from '../../parameters/components/parameter-list';

const CHANNEL = gql`
    query Channel($instrumentAddress: String!, $channelName: String!) {
        instrument(address: $instrumentAddress) {
            channel(name: $channelName) {
                name
                parameters {
                    name
                }
            }
        }
    }
`;

export function SingleChannel() {
    const { instrumentAddress, channelName } = useParams();
    const { data, loading } = useQuery(CHANNEL, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.'),
            channelName
        }
    });

    if (loading) { return 'Loading'; }
    
    return (
        <>
            <h2>{ channelName }</h2>
            <ParameterList parameters={data.instrument.channel.parameters} />
        </>
    );
}
