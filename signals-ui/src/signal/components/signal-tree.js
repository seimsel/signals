import React from 'react';
import { Tree } from 'antd';
import { useQuery } from '@apollo/client';
import { useQueryParams } from '../../common/hooks/use-query-params';
import signalTreeQuery from '../queries/signal-tree.graphql';

function create_tree(nodes) {
    return nodes.map(node => ({
        ...node,
        children: get_children(node, nodes),
        title: node.name,
        key: node.id
    }));
}

function get_children(parent, nodes) {
    const childIds = parent.children.map(child => child.id);
    const children = nodes.filter(node => childIds.includes(node.id));

    return children.map(child => ({
        ...child,
        children: get_children(child, nodes),
        title: child.name,
        key: `${parent.id}-${child.id}`
    }));
}

export function SignalTree() {
    const params = useQueryParams();
    const { data, loading } = useQuery(signalTreeQuery, {
        variables: {
            url: params.get('url')
        }
    });

    if (loading) {
        return 'Loading...';
    }

    if (!data) {
        return null;
    }

    const signals = data.measurement.children;

    return (
        <Tree 
            treeData={ create_tree(signals) }
        />
    );
}
