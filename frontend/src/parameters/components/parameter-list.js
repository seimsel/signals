import React from 'react';
import { useParams } from 'react-router';
import { Link } from 'react-router-dom';

export function ParameterList({ parameters }) {
    const { instrumentAddress, channelName } = useParams();

    return (
        <ul>
            {
                parameters.map(parameter => (
                    <Link key={parameter.name}to={`/instruments/${instrumentAddress}/channels/${channelName}/parameters/${parameter.name}`}>
                        <li>
                            { parameter.name }
                        </li>
                    </Link>
                ))
            }
            <Link key='back' to={`/instruments/${instrumentAddress}`}><li>Back to Instrument</li></Link>
        </ul>
    );
}
