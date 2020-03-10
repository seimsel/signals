import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useParams, useHistory } from 'react-router';
import { PageHeader } from 'antd';
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
    const history = useHistory()
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
            <PageHeader
                title={channelName}
                onBack={() => history.push(`/instruments/${instrumentAddress}`)}
            />
            <ParameterList parameters={data.instrument.channel.parameters} />
        </>
    );
}
