import React from 'react';
import gql from 'graphql-tag';
import { useQuery, useMutation } from '@apollo/client';
import { useParams } from 'react-router';
import { List, Button, Row, Col } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const CHANNEL_TYPES = gql`
    query ChannelTypes($instrumentAddress: String!) {
        instrument(address: $instrumentAddress) {
            id
            channelTypes {
                id
                name
            }
        }
    }
`;

const CREATE_CHANNEL = gql`
    mutation CreateChannel($instrumentAddress: String!, $channelTypeName: String!) {
        createChannel(
            instrumentAddress: $instrumentAddress,
            channelTypeName: $channelTypeName
        ) {
            id
            name
        }
    }
`;

const CHANNELS = gql`
    query Channels($instrumentAddress: String!) {
        instrument(address: $instrumentAddress) {
            id
            channels {
                id
                name
            }
        }
    }
`;

export function ChannelTypeList() {
    const { instrumentAddress } = useParams();
    const { data, loading } = useQuery(CHANNEL_TYPES, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.')
        }
    });
    const [ createChannel ] = useMutation(CREATE_CHANNEL, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.')
        },
        update: (cache, { data: { createChannel } }) => {
            let cachedData = null;
            try {
                cachedData = cache.readQuery({
                    query: CHANNELS,
                    variables: {
                        instrumentAddress: instrumentAddress.replace(/_/g, '.')
                    }
                });
            } catch {
                return;
            }

            cache.writeQuery({
                query: CHANNELS,
                variables: {
                    instrumentAddress: instrumentAddress.replace(/_/g, '.')
                },
                data: {
                    instrument: {
                        ...cachedData.instrument,
                        channels: [
                            ...cachedData.instrument.channels,
                            createChannel
                        ]
                    }
                }
            })
        }
    })

    const channelTypes = data ? data.instrument.channelTypes : [];

    return (
        <List
            loading={loading}
            dataSource={channelTypes}
            renderItem={channelType => (
                <List.Item
                    extra={<PlusOutlined />}
                    key={channelType.name}
                    title={channelType.name}
                    onClick={() => createChannel({
                        variables: {
                            channelTypeName: channelType.name
                        }
                    })}
                >
                    <List.Item.Meta
                        title={channelType.name}
                    />
                </List.Item>
            )}
        />
    );
}