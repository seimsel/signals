import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Layout } from 'antd';
import { ApiProvider } from '../../api/components/api-provider';
import { Sider } from './sider';
import { Content } from './content';

function Main() {
    return (
        <Layout
            style={{ height:"100vh" }}
        >
            <Layout>
                <Layout.Sider
                    width={300}
                    collapsible
                    collapsedWidth={0}
                >
                    <Sider />
                </Layout.Sider>
                <Layout.Content>
                    <Content />
                </Layout.Content>
            </Layout>
        </Layout>
    );
}

export function App() {
    return (
        <Router>
            <ApiProvider>
                <Main />
            </ApiProvider>
        </Router>
    );
}
