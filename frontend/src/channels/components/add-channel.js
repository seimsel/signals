import React from 'react';
import { useParams, useHistory } from 'react-router';
import { PageHeader } from 'antd';
import { ChannelTypeList } from './channel-type-list';

export function AddChannel() {
    const history = useHistory()
    const { instrumentAddress } = useParams();
    
    return (
        <>
            <PageHeader
                title={'Channel Types'}
                onBack={() => history.push(`/instruments/${instrumentAddress}`)}
            />
            <ChannelTypeList />
        </>
    );
}
