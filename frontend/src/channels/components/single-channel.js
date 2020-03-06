import React from 'react';
import { useParams } from 'react-router';
import { Link } from 'react-router-dom';

export function SingleChannel() {
    const { name } = useParams();
    
    return (
        <>
            <h2>{ name }</h2>
            <ul>
                
            </ul>
            <Link to='/'>{'Back to Instrument'}</Link>
        </>
    );
}
