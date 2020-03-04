import React from 'react';
import gql from 'graphql-tag';
import { useQuery } from '@apollo/react-hooks';

const LIST_FUNCTIONS = gql`
    query ListFunctions($address: String!) {
        functions(instrumentAddress: $address) {
            name
            instrumentAddress
        }
    }
`;

export function FunctionList({ address }) {
    const { data, loading } = useQuery(LIST_FUNCTIONS, {
        variables: {
            address
        }
    });

    return (
        <ul>
        {
            data ? data.functions.map(f => (
                <li key={f.address}>
                    { f.name }
                </li>
            )) : null
        }
        </ul>
    );
}
