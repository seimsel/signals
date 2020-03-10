import React from 'react';
import { useParams, useHistory } from 'react-router';
import { List } from 'antd';
import { RightOutlined } from '@ant-design/icons';

export function ChannelList({ channels, ...props }) {
    const history = useHistory();
    const { instrumentAddress } = useParams();

    return (
        <List
            dataSource={channels}
            renderItem={channel => (
                <List.Item
                    extra={<RightOutlined />}
                    key={channel.name}
                    onClick={() => history.push(`/instruments/${instrumentAddress}/channels/${channel.name}`)}
                >
                    { channel.name }
                </List.Item>
            )}
            {...props}
        />
    );
}
