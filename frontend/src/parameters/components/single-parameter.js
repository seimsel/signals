import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useParams } from 'react-router';
import { Link } from 'react-router-dom';

const PARAMETER = gql`
    query Parameter($instrumentAddress: String!, $channelName: String!, $parameterName: String!) {
        instrument(address: $instrumentAddress) {
            channel(name: $channelName) {
                parameter(name: $parameterName) {
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

function Editor({ parameter }) {
    switch (parameter.__typename) {
        case 'IntegerParameter':
            return <input defaultValue={parameter.value} />

        case 'FloatParameter':
            return <input defaultValue={parameter.value} />

        case 'SelectParameter':
            return (
                <select defaultValue={parameter.value}>
                    {
                        parameter.options.map(option => (
                            <option>{ option }</option>
                        ))
                    }
                </select>
            )
    
        default:
            return parameter.value;
    }
}

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
            <Editor parameter={data.instrument.channel.parameter} />
            <Link to={`/instruments/${instrumentAddress}/channels/${channelName}`}>{`Back to ${channelName}`}</Link>
        </>
    );
}
