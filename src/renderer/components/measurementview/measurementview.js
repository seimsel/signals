import React from 'react';

export function MeasurementView({ measurement }) {
    return <ul>
        {
            measurement.channels.map(ch => <li key={ch.id}>{ch.name}</li>)
        }
    </ul>;
}
