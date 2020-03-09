import React from 'react';
import { useParams, useHistory } from 'react-router';
import { Link } from 'react-router-dom';
import { List } from 'antd';

export function ChannelList({ channels }) {
    const history = useHistory();
    const { instrumentAddress } = useParams();

    return (
        <List
            dataSource={channels}
            renderItem={channel => (
                <List.Item
                    key={channel.name}
                    onClick={() => history.push(`/instruments/${instrumentAddress}/channels/${channel.name}`)}
                >
                    { channel.name }
                </List.Item>
            )}
        />
    );
}
