import React from 'react';
import gql from 'graphql-tag';
import { useQuery, useMutation } from '@apollo/client';
import { useParams } from 'react-router';
import { List, InputNumber, Select } from 'antd';

const PARAMETERS = gql`
    query Parameters($instrumentAddress: String!, $channelName: String!) {
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
                    ... on SourceParameter {
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
            id
            name
            value
        }
    }
`;

function Editor({ instrumentAddress, channelName, parameter }) {
    const [ update ] = useMutation(UPDATE_PARAMETER, {
        variables: {
            instrumentAddress,
            channelName,
            parameterName: parameter.name
        }
    });

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
        case 'SourceParameter':
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

export function ParameterList() {
    const { instrumentAddress, channelName } = useParams();
    const { data, loading } = useQuery(PARAMETERS, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.'),
            channelName
        }
    });

    const parameters = data ? data.instrument.channel.parameters : [];

    return (
        <List
            loading={loading}
            itemLayout='vertical'
            dataSource={parameters}
            renderItem={parameter => (
                <List.Item
                    key={parameter.name}
                >
                    <List.Item.Meta
                        title={parameter.name}
                    />
                    <Editor
                        instrumentAddress={instrumentAddress}
                        channelName={channelName}
                        parameter={parameter}
                    />
                </List.Item>
            )}
        />
    );
}
