import React from 'react';
import gql from 'graphql-tag';
import { Link } from 'react-router-dom';
import { useQuery } from '@apollo/react-hooks';

const LIST_CHANNELS = gql`
    query ListChannels($address: String!) {
        instrument(address: $address) {
            channels {
                name
            }
        }
    }
`;

export function ChannelList({ address }) {
    const { data, loading } = useQuery(LIST_CHANNELS, {
        variables: {
            address
        }
    });

    return (
        <ul>
        {
            data ? data.instrument.channels.map(channel => (
                <Link to={`/channels/${channel.name}`}>
                    <li key={channel.name}>
                        { channel.name }
                    </li>
                </Link>
            )) : null
        }
        </ul>
    );
}
