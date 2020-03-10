import React from 'react';
import { useParams, useHistory } from 'react-router';
import { PageHeader } from 'antd';
import { ParameterList } from '../../parameters/components/parameter-list';


export function SingleChannel() {
    const history = useHistory()
    const { instrumentAddress, channelName } = useParams();
    
    return (
        <>
            <PageHeader
                title={channelName}
                onBack={() => history.push(`/instruments/${instrumentAddress}`)}
            />
            <ParameterList />
        </>
    );
}
