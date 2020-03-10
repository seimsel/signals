import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useParams, useHistory } from 'react-router';
import { PageHeader } from 'antd';
import { ParameterList } from '../../parameters/components/parameter-list';

const CHANNEL = gql`
    query Channel($instrumentAddress: String!, $channelName: String!) {
        instrument(address: $instrumentAddress) {
            id
            channel(name: $channelName) {
                id
                name
                parameters {
                    id
                    name
                    value
                    ... on IntegerParameter {
                        lowerLimit
                        upperLimit
                    }
                    ... on SelectParameter {
                        options
                    }
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
    
    return (
        <>
            <PageHeader
                title={channelName}
                onBack={() => history.push(`/instruments/${instrumentAddress}`)}
            />
            <ParameterList
                parameters={data ? data.instrument.channel.parameters : []}
                loading={loading}
            />
        </>
    );
}
