import React from 'react';
import gql from 'graphql-tag';
import { useParams } from 'react-router';
import { useQuery } from '@apollo/client';
import { ChannelList } from '../../channels/components/channel-list';

const INSTRUMENT = gql`
    query Instrument($address: String!) {
        instrument(address: $address) {
            channels {
                name
            }
        }
    }
`;

export function SingleInstrument() {
    const { instrumentAddress } = useParams();
    const { data, loading } = useQuery(INSTRUMENT, {
        variables: {
            address: instrumentAddress.replace(/_/g, '.')
        }
    });

    if (loading) { return 'Loading'; }

    return (
        <>
            <h2>Channels</h2>
            <ChannelList channels={data.instrument.channels} />
        </>
    );
}
