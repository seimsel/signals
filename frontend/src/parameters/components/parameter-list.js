import React from 'react';
import { useParams } from 'react-router';
import { Link } from 'react-router-dom';

export function ParameterList({ parameters }) {
    const { instrumentAddress, channelName } = useParams();
    console.log(parameters)

    return (
        <ul>
            {
                parameters.map(parameter => (
                    <Link to={`/instruments/${instrumentAddress}/channels/${channelName}/parameters/${parameter.name}`}>
                        <li key={parameter.name}>
                            { parameter.name }
                        </li>
                    </Link>
                ))
            }
        </ul>
    );
}
