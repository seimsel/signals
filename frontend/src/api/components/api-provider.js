import React from 'react';
import { ApolloClient, ApolloProvider, ApolloLink, InMemoryCache, HttpLink, split } from '@apollo/client';
import { WebSocketLink } from 'apollo-link-ws';
import { onError } from 'apollo-link-error';
import { getMainDefinition } from 'apollo-utilities';

const httpLink = new HttpLink({
    uri: `${process.env.BACKEND_HTTP_URL}/graphql/`
});

const wsLink = new WebSocketLink({
    uri: `${process.env.BACKEND_WS_URL}/graphql/`,
    options: {
        reconnect: true
    }
});

const link = split(
    ({ query }) => {
        const definition = getMainDefinition(query);
        return (
            definition.kind === 'OperationDefinition' &&
            definition.operation === 'subscription'
        );
    },
    wsLink,
    httpLink,
);

const errorHandler = onError(({ graphQLErrors, networkError }) => {
    if (graphQLErrors)
        for (let { message, locations, path } of graphQLErrors) {
            console.error(
                `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
            )
        }
    if (networkError) console.error(`[Network error]: ${networkError}`);
});

const client = new ApolloClient({
    defaultOptions: {
        watchQuery: {
            errorPolicy: 'all'
        }
    },
    link: ApolloLink.from([
        errorHandler,
        link
    ]),
    cache: new InMemoryCache({
        possibleTypes: {
            'Parameter': [
                'IntegerParameter',
                'SelectionParameter'
            ]
        }
    })
});

export function ApiProvider({ children }) {
    return (
        <ApolloProvider client={client}>
            {children}
        </ApolloProvider>
    );
}
