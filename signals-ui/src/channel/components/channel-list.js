import React from 'react';
import { List } from 'antd';

export function ChannelList({ channels }) {
    return (
        <List>
        {
            channels.map(({ name }) => (
                <List.Item>
                    { name }
                </List.Item>
            ))
        }
        </List>
    );
}
