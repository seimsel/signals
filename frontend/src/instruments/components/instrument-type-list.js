import React from 'react';
import gql from 'graphql-tag';
import { useMutation, useQuery } from '@apollo/client';
import { List } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const INSTRUMENT_TYPES = gql`
    query InstrumentTypes {
        instrumentTypes {
            id
            name
        }
    }
`;

const CREATE_INSTRUMENT = gql`
    mutation CreateInstrument($address: String, $instrumentTypeName: String!) {
        createInstrument(
            address: $address,
            instrumentTypeName: $instrumentTypeName
        ) {
            id
            address
        }
    }
`;

const INSTRUMENTS = gql`
    query Instruments($instrumentAddress: String!) {
        instruments {
            id
            address
        }
    }
`;

export function InstrumentTypeList() {
    const { data, loading } = useQuery(INSTRUMENT_TYPES);
    const [ createInstrument ] = useMutation(CREATE_INSTRUMENT, {
        update: (cache, { data: { createInstrument } }) => {
            let cachedData = null;
            try {
                cachedData = cache.readQuery({
                    query: INSTRUMENTS
                });
            } catch(e) {
                return;
            }

            cache.writeQuery({
                query: INSTRUMENTS,
                data: {
                    instruments: [
                        ...cachedData.instruments,
                        createInstrument
                    ]
                }
            })
        }
    })

    const instrumentTypes = data ? data.instrumentTypes : [];

    return (
        <List
            loading={loading}
            dataSource={instrumentTypes}
            renderItem={instrumentType => (
                <List.Item
                    extra={<PlusOutlined />}
                    key={instrumentType.name}
                    title={instrumentType.name}
                    onClick={() => createInstrument({
                        variables: {
                            address: '',
                            instrumentTypeName: instrumentType.name
                        }
                    })}
                >
                    <List.Item.Meta
                        title={instrumentType.name}
                    />
                </List.Item>
            )}
        />
    );
}
