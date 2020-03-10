import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useParams, useHistory } from 'react-router';
import { List, Button, Row, Col } from 'antd';
import { RightOutlined, PlusOutlined } from '@ant-design/icons';

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

export function ChannelList() {
    const history = useHistory();
    const { instrumentAddress } = useParams();
    const { data, loading } = useQuery(CHANNELS, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.')
        }
    });

    const channels = data ? data.instrument.channels : [];

    return (
        <List
            loading={loading}
            dataSource={channels}
            footer={
                <Row
                    justify='center'
                >
                    <Col>
                        <Button
                            icon={<PlusOutlined />}
                            onClick={() => history.push(`/instruments/${instrumentAddress}/channels/add`)}
                        >
                            Add Channel
                        </Button>
                    </Col>
                </Row>
            }
            renderItem={channel => (
                <List.Item
                    extra={<RightOutlined />}
                    key={channel.name}
                    title={channel.name}
                    onClick={() => history.push(`/instruments/${instrumentAddress}/channels/${channel.name}`)}
                >
                    <List.Item.Meta
                        title={channel.name}
                    />
                </List.Item>
            )}
        />
    );
}
