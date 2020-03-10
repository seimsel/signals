import React from 'react';
import { useParams } from 'react-router';
import gql from 'graphql-tag';
import { useMutation } from '@apollo/client';
import { List, InputNumber, Select } from 'antd';

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

export function ParameterList({ parameters, ...props }) {
    const { instrumentAddress, channelName } = useParams();

    return (
        <List
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
            {...props}
        />
    );
}
