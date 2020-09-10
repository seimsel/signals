import React from 'react';
import { Typography, Skeleton } from 'antd';
import { SignalTree } from '../../signal/components/signal-tree';

export function Sider({ measurement, loading }) {
    if (loading) {
        return (
            <Skeleton />
        );
    }

    const { children } = measurement;

    return (
        <SignalTree signals={ children } />
    );
}
