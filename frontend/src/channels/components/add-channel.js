import React from 'react';
import { useParams, useHistory } from 'react-router';
import { PageHeader } from 'antd';
import { AvailableChannelList } from './available-channel-list';

export function AddChannel() {
    const history = useHistory()
    const { instrumentAddress } = useParams();
    
    return (
        <>
            <PageHeader
                title={'Available Channels'}
                onBack={() => history.push(`/instruments/${instrumentAddress}`)}
            />
            <AvailableChannelList />
        </>
    );
}
