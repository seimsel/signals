import React from 'react';
import gql from 'graphql-tag';
import { useHistory } from 'react-router';
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
    const history = useHistory();
    const { data, loading } = useQuery(INSTRUMENT_TYPES);
    const [ createInstrument, { loading: creating } ] = useMutation(CREATE_INSTRUMENT, {
        onCompleted: ({ createInstrument: { address }}) => history.push(`/instruments/${address}`),
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
            loading={loading || creating}
            dataSource={instrumentTypes}
            renderItem={instrumentType => (
                <List.Item
                    className='clickable'
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
