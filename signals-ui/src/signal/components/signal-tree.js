import React from 'react';
import { Tree } from 'antd';

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

export function SignalTree({ signals }) {
    const tree = create_tree(signals);
    console.log(tree)

    return (
        <Tree 
            treeData={ tree }
        />
    );
}
