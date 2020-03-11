import React from 'react';
import { PageHeader } from 'antd';
import { InstrumentList } from '../../instruments/components/instrument-list';

export function Welcome() {
    return (
        <>
            <PageHeader
                title='Instruments'
            />
            <InstrumentList />
        </>
    );
}
