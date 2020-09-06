import React from 'react';
import { useQuery } from '@apollo/client';
import { Tree } from 'antd';
import treeViewQuery from '../queries/tree-view.graphql';

function create_tree(nodes) {

    return tree;
}

export function TreeView() {
    const { data } = useQuery(treeViewQuery);
    
    let treeData = [];

    if (data) {
        console.log(create_tree(data.nodes));
        // treeData = create_tree(nodes);
    }

    return (
        <Tree
            treeData={ treeData }
        />
    );
}
