import React from 'react';
import { Typography, Skeleton } from 'antd';
import { SignalTree } from '../../signal/components/signal-tree';

export function Sider({ measurement, loading }) {
    if (loading) {
        return (
            <Skeleton />
        );
    }

    const { name, children } = measurement;

    return (
        <>
            <Typography.Title
                level={2}
            >
                { name }
            </Typography.Title>
            <SignalTree signals={ children } />
        </>
    );
}
