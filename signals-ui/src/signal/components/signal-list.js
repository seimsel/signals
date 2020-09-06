import React from 'react';
import { List } from 'antd';

export function SignalList({ signals }) {
    return (
        <List>
        {
            signals.map(({ name }) => (
                <List.Item>
                    { name }
                </List.Item>
            ))
        }
        </List>
    );
}
