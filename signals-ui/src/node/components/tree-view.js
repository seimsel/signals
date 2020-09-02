import React from 'react';
import { useQuery } from '@apollo/client';
import { Tree } from 'antd';
import treeViewQuery from '../queries/tree-view.gql';
import childrenQuery from '../queries/children.gql';

function map_tree(node, func) {
    const mapped_node = func(node);

    if (!node.children) {
        return mapped_node;
    }

    let children = [];

    for (let child of node.children) {
        children.push(map_tree(child, func));
    }

    return {
        ...mapped_node,
        children
    }
}

export function TreeView() {
    const { data, loading, fetchMore } = useQuery(treeViewQuery);
    
    let treeData = [];

    console.log('render');

    if (!loading) {
        const { measurement } = data;
        treeData = [
            map_tree(data.measurement, node => ({
                title: node.id,
                key: node.id,
                isLeaf: node.childCount === 0
            }))
        ];
    }

    async function loadData(node) {
        await fetchMore({
            query: childrenQuery,
            variables: {
                nodeId: node.key
            },
            updateQuery: ({ measurement }, { fetchMoreResult }) => ({
                measurement: map_tree(measurement, n => {
                    if (n.id === node.key) {
                        return {
                            ...n,
                            children: fetchMoreResult.node.children
                        };
                    }

                    return n;
                })
            })
        });
    }

    return (
        <Tree
            treeData={ treeData }
            loadData={ loadData }
        />
    );
}
