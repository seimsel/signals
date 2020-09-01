import React from 'react';
import { useQuery, useApolloClient } from '@apollo/client';
import { Tree } from 'antd';
import treeViewQuery from '../queries/tree-view.gql';
import childrenQuery from '../queries/children.gql';

async function loadData(node, client) {
    return await client.query({
        query: childrenQuery,
        variables: {
            nodeId: node.key
        }
    });
}

export function TreeView() {
    const client = useApolloClient();
    const { data, loading } = useQuery(treeViewQuery);

    let treeData = [];

    if (!loading) {
        const { measurement } = data;

        treeData = [
            {
                title: measurement.url,
                isLeaf: measurement.childCount <= 0,
                key: measurement.id
            }
        ]
    }

    return (
        <Tree
            treeData={ treeData }
            loadData={ node => loadData(node, client) }
        />
    );
}
