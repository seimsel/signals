import React from 'react';
import { useQuery } from '@apollo/client';
import { Tree } from 'antd';
import treeViewQuery from '../queries/tree-view.gql';

export function TreeView() {
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
        />
    );
}
