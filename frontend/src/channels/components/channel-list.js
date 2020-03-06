import React from 'react';
import { useParams } from 'react-router';
import { Link } from 'react-router-dom';

export function ChannelList({ channels }) {
    const { instrumentAddress } = useParams();

    return (
        <ul>
        {
            channels.map(channel => (
                <Link to={`/instruments/${instrumentAddress}/channels/${channel.name}`}>
                    <li key={channel.name}>
                        { channel.name }
                    </li>
                </Link>
            ))
        }
        </ul>
    );
}
