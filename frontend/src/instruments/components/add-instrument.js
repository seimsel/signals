import React from 'react';
import { useHistory } from 'react-router';
import { PageHeader } from 'antd';
import { InstrumentTypeList } from './instrument-type-list';

export function AddInstrument() {
    const history = useHistory();
    
    return (
        <>
            <PageHeader
                title={'Instrument Types'}
                onBack={() => history.push('/')}
            />
            <InstrumentTypeList />
        </>
    );
}
