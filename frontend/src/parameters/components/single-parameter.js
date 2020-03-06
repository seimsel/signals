import React from 'react';
import gql from 'graphql-tag';
import { useParams } from 'react-router';
import { useQuery } from '@apollo/react-hooks';


const PARAMETER = gql`
    query Parameter($instrumentAddress: String!, $channelName: String!, $parameterName: String!) {
        instrument(address: $instrumentAddress) {
            channel(name: $channelName) {
                parameter(name: $parameterName) {
                    value
                }
            }
        }
    }
`;

export function SingleParameter() {
    const { instrumentAddress, channelName, parameterName } = useParams();
    const { data, loading } = useQuery(PARAMETER, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.'),
            channelName,
            parameterName
        }
    });


    if (loading) { return 'Loading'; }

    return (
        <>
            <h2>{ parameterName }</h2>
            <input defaultValue={data.instrument.channel.parameter.value} />
        </>
    );
}
