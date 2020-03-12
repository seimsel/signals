import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/client';
import { useHistory } from 'react-router';
import { List, Button, Row, Col } from 'antd';
import { RightOutlined, PlusOutlined } from '@ant-design/icons';

const INSTRUMENTS = gql`
    query Instruments {
        instruments {
            id
            address
        }
    }
`;

export function InstrumentList() {
    const history = useHistory();
    const { data, loading } = useQuery(INSTRUMENTS);

    const instruments = data ? data.instruments : [];

    return (
        <List
            loading={loading}
            dataSource={instruments}
            footer={
                <Row
                    justify='center'
                >
                    <Col>
                        <Button
                            icon={<PlusOutlined />}
                            onClick={() => history.push('/instruments/add')}
                        >
                            Add Instrument
                        </Button>
                    </Col>
                </Row>
            }
            renderItem={instrument => (
                <List.Item
                    className='clickable'
                    extra={<RightOutlined />}
                    key={instrument.address}
                    title={instrument.address}
                    onClick={() => history.push(`/instruments/${instrument.address}`)}
                >
                    <List.Item.Meta
                        title={instrument.address}
                    />
                </List.Item>
            )}
        />
    );
}
