import React from 'react';
import { Layout, Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import { useQuery } from '@apollo/client';
import { ApiProvider } from '../../api/components/api-provider';
import { Menubar } from './menubar';
import { Sider } from './sider';
import { Content } from './content';
import sessionQuery from '../queries/session.graphql';

function Main() {
    const { loading } = useQuery(sessionQuery);

    return (
        <Spin
            indicator={
                <LoadingOutlined
                    style={{
                        fontSize: '10em'
                    }}
                    spin
                />
            }
            spinning={ loading }
        >
            <Layout
                style={{ height:"100vh" }}
            >
                <Layout.Header
                    style={{ padding: 0 }}
                >
                    { loading ? null : <Menubar /> }
                </Layout.Header>
                <Layout>
                    <Layout.Sider
                        width={300}
                        collapsible
                        collapsedWidth={0}
                    >
                        { loading ? null : <Sider /> }
                    </Layout.Sider>
                    <Layout.Content>
                        { loading ? null : <Content /> }
                    </Layout.Content>
                </Layout>
            </Layout>
        </Spin>
    );
}

export function App() {


    return (
        <ApiProvider>
            <Main />
        </ApiProvider>
    );
}
