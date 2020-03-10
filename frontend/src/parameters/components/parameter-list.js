import React from 'react';
import { useParams, useHistory } from 'react-router';
import { List } from 'antd';
import { RightOutlined } from '@ant-design/icons';

export function ParameterList({ parameters, ...props }) {
    const history = useHistory();
    const { instrumentAddress, channelName } = useParams();

    return (
        <List
            dataSource={parameters}
            renderItem={parameter => (
                <List.Item
                    extra={<RightOutlined />}
                    key={parameter.name}
                    onClick={() => history.push(`/instruments/${instrumentAddress}/channels/${channelName}/parameters/${parameter.name}`)}
                >
                    { parameter.name }
                </List.Item>
            )}
            {...props}
        />
    );
}
