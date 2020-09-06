import React from 'react';
import { Typography, Skeleton } from 'antd';
import { useQuery } from '@apollo/client';
import { SignalList } from '../../signal/components/signal-list';
import measurementQuery from '../queries/measurement.graphql';

export function Sider() {
    const { data } = useQuery(measurementQuery);

    if (!data) {
        return (
            <Skeleton />
        );
    }

    const { name, children } = data.session.windows[0].measurements[0];

    return (
        <>
            <Typography.Title
                level={2}
            >
                { name }
            </Typography.Title>
            <SignalList
                signals={ children }
            />
        </>
    );
}
