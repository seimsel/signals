import React from 'react';
import { Figure } from '../../figure/components/figure';

export function Content({ measurement }) {
    return <Figure measurementId={ measurement.id } />
}
