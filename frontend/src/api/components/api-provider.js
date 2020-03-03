import React from 'react';
import { ApolloClient } from 'apollo-client';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { HttpLink } from 'apollo-link-http';
import { WebSocketLink } from 'apollo-link-ws';
import { onError } from 'apollo-link-error';
import { ApolloLink, split } from 'apollo-link';
import { getMainDefinition } from 'apollo-utilities';
import { ApolloProvider } from '@apollo/react-hooks';

const httpLink = new HttpLink({
    uri: 'http://localhost:8000/graphql/'
});

const wsLink = new WebSocketLink({
    uri: 'ws://localhost:8000/graphql/',
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
    cache: new InMemoryCache()
});

export function ApiProvider({ children }) {
    return (
        <ApolloProvider client={client}>
            {children}
        </ApolloProvider>
    );
}
