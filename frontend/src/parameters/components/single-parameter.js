import React from 'react';
import gql from 'graphql-tag';
import { useQuery, useMutation } from '@apollo/client';
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

const UPDATE_PARAMETER = gql`
    mutation UpdateParameter(
        $instrumentAddress: String!,
        $channelName: String!,
        $parameterName: String!,
        $value: Value!
    ) {
        updateParameter(
            instrumentAddress: $instrumentAddress
            channelName: $channelName
            parameterName: $parameterName
            value: $value
        ) {
            success
            errorMessage
        }
    }
`;

function Editor({ parameter, update }) {
    switch (parameter.__typename) {
        case 'IntegerParameter':
            return (
                <input
                    defaultValue={parameter.value}
                    onKeyPress={({ key, target: { value }}) => {
                        if (key === 'Enter') {
                            update({
                                variables: {
                                    value: parseInt(value)
                                }
                            })
                        }
                    }}
                />
            )

        case 'FloatParameter':
            return (
                <input
                    defaultValue={parameter.value}
                    onKeyPress={({ key, target: { value }}) => {
                        if (key === 'Enter') {
                            update({
                                variables: {
                                    value: parseFloat(value)
                                }
                            })
                        }
                    }}
                />
            )

        case 'SelectParameter':
            return (
                <select defaultValue={parameter.value}
                    onChange={({ target: { value }}) => update({
                        variables: {
                            value
                        }
                    })}
                >
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
    const [ update ] = useMutation(UPDATE_PARAMETER, {
        variables: {
            instrumentAddress,
            channelName,
            parameterName
        }
    })

    if (loading) { return 'Loading'; }

    return (
        <>
            <h2>{ parameterName }</h2>
            <Editor parameter={data.instrument.channel.parameter} update={update} />
            <Link to={`/instruments/${instrumentAddress}/channels/${channelName}`}>{`Back to ${channelName}`}</Link>
        </>
    );
}
