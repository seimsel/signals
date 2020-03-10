import React from 'react';
import gql from 'graphql-tag';
import { useQuery, useMutation } from '@apollo/client';
import { useParams, useHistory } from 'react-router';
import { PageHeader, InputNumber, Select, Spin } from 'antd';

const PARAMETER = gql`
    query Parameter($instrumentAddress: String!, $channelName: String!, $parameterName: String!) {
        instrument(address: $instrumentAddress) {
            id
            channel(name: $channelName) {
                id
                parameter(name: $parameterName) {
                    id
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

function Editor({ parameter, update, loading }) {
    if (loading) {
        return <Spin spinning={true} />
    }

    switch (parameter.__typename) {
        case 'IntegerParameter':
            return (
                <InputNumber
                    defaultValue={parameter.value}
                    onChange={value => {
                        if (value === '') {
                            return;
                        }
                        update({
                            variables: {
                                value: parseInt(value)
                            }
                        })
                    }}
                />
            )

        case 'FloatParameter':
            return (
                <InputNumber
                    defaultValue={parameter.value}
                    onChange={value => {
                        if (value === '') {
                            return;
                        }
                        update({
                            variables: {
                                value: parseFloat(value)
                            }
                        })
                    }}
                />
            )

        case 'SelectParameter':
            return (
                <Select
                    defaultValue={parameter.value}
                    onChange={value => update({
                        variables: {
                            value
                        }
                    })}
                >
                    {
                        parameter.options.map(option => (
                            <Select.Option
                                key={option}
                            >
                                { option }
                            </Select.Option>
                        ))
                    }
                </Select>
            )
    
        default:
            return parameter.value;
    }
}

export function SingleParameter() {
    const history = useHistory();
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

    return (
        <>
            <PageHeader
                title={parameterName}
                onBack={() => history.push(`/instruments/${instrumentAddress}/channels/${channelName}`)}
            />
            <Editor
                parameter={data ? data.instrument.channel.parameter : {}}
                update={update}
                loading={loading}
            />
        </>
    );
}
