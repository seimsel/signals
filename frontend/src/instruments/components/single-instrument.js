import React from 'react';
import { useParams } from 'react-router';
import { PageHeader } from 'antd';
import { ChannelList } from '../../channels/components/channel-list';

export function SingleInstrument() {
    const { instrumentAddress } = useParams();

    return (
        <>
            <PageHeader
                title={instrumentAddress}
            />
            <ChannelList />
        </>
    );
}
