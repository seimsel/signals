import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useParams, useHistory } from 'react-router';
import { List, Button, Row, Col } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const AVAILABLE_CHANNELS = gql`
    query AvailableChannels($instrumentAddress: String!) {
        instrument(address: $instrumentAddress) {
            id
            availableChannels {
                id
                name
            }
        }
    }
`;

export function AvailableChannelList() {
    const history = useHistory();
    const { instrumentAddress } = useParams();
    const { data, loading } = useQuery(AVAILABLE_CHANNELS, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.')
        }
    });

    const availableChannels = data ? data.instrument.availableChannels : [];

    return (
        <List
            loading={loading}
            dataSource={availableChannels}
            renderItem={channel => (
                <List.Item
                    extra={<PlusOutlined />}
                    key={channel.name}
                    title={channel.name}
                >
                    <List.Item.Meta
                        title={channel.name}
                    />
                </List.Item>
            )}
        />
    );
}
