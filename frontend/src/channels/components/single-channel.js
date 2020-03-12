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

export function SingleChannel() {
    const history = useHistory()
    const { instrumentAddress, channelName } = useParams();
    const [ deleteChannel ] = useMutation(DELETE_CHANNEL, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.'),
            channelName
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
