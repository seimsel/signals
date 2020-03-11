import React from 'react';
import { useHistory, useParams } from 'react-router';
import { PageHeader } from 'antd';
import { ChannelList } from '../../channels/components/channel-list';

export function SingleInstrument() {
    const history = useHistory();
    const { instrumentAddress } = useParams();

    return (
        <>
            <PageHeader
                title={instrumentAddress}
                onBack={() => history.push('/')}
            />
            <ChannelList />
        </>
    );
}
