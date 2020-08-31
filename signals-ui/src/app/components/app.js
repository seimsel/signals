import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Switch, Route } from 'react-router';
import { Layout } from 'antd';
import { ApiProvider } from '../../api/components/api-provider';
import { Sider } from './sider';

export function App() {
    return (
        <ApiProvider>
            <Router>
                <Layout style={{height:"100vh"}}>
                    <Layout.Sider
                        width={300}
                        collapsible
                        collapsedWidth={0}
                    >
                        <Sider />
                    </Layout.Sider>
                    <Layout.Content>
                        <Switch>
                            <Route exact path='/' component={() => null} />
                        </Switch>
                    </Layout.Content>
                </Layout>
            </Router>
        </ApiProvider>
    );
}
