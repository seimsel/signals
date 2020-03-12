import React from 'react';
import gql from 'graphql-tag';
import { useParams, useHistory } from 'react-router';
import { useMutation } from '@apollo/client';
import { PageHeader, Button, Row, Col } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import { ParameterList } from '../../parameters/components/parameter-list';

const DELETE_CHANNEL = gql`
    mutation DeleteChannel(
        $instrumentAddress: String!,
        $channelName: String!
    ) {
        deleteChannel(
            instrumentAddress: $instrumentAddress,
            channelName: $channelName
        ) {
            id
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

export function SingleChannel() {
    const history = useHistory()
    const { instrumentAddress, channelName } = useParams();
    const [ deleteChannel, { loading:deleting } ] = useMutation(DELETE_CHANNEL, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.'),
            channelName
        },
        onCompleted: () => history.push(`/instruments/${instrumentAddress}`),
        update: (cache, { data: { deleteChannel } }) => {
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
                        channels: cachedData.instrument.channels.filter(
                            channel => channel.id != deleteChannel.id
                        )
                    }
                }
            })
        }
    });

    return (
        <>
            <PageHeader
                title={channelName}
                onBack={() => history.push(`/instruments/${instrumentAddress}`)}
            />
            <ParameterList />
            <Row
                    justify='center'
                >
                <Col>
                    <Button
                        type='danger'
                        icon={<DeleteOutlined />}
                        loading={deleting}
                        onClick={() => {
                            deleteChannel();
                        }}
                    >
                        {`Remove ${channelName}`}
                    </Button>
                </Col>
            </Row>
        </>
    );
}
