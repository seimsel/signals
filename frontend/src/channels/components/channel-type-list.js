import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useParams, useHistory } from 'react-router';
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

export function ChannelTypeList() {
    const history = useHistory();
    const { instrumentAddress } = useParams();
    const { data, loading } = useQuery(CHANNEL_TYPES, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.')
        }
    });

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
                >
                    <List.Item.Meta
                        title={channelType.name}
                    />
                </List.Item>
            )}
        />
    );
}
