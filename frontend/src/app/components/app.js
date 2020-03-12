import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Switch, Route } from 'react-router';
import { Layout } from 'antd';
import { ApiProvider } from '../../api/components/api-provider';
import { SingleInstrument } from '../../instruments/components/single-instrument';
import { SingleChannel } from '../../channels/components/single-channel';
import { AddChannel } from '../../channels/components/add-channel';
import { Figure } from '../../figure/components/figure';
import { Welcome } from './welcome';
import { AddInstrument } from '../../instruments/components/add-instrument';

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
                        <Switch>
                            <Route exact path='/' component={Welcome} />
                            <Route path='/instruments/add' component={AddInstrument} />
                            <Route path='/instruments/:instrumentAddress/channels/add' component={AddChannel} />
                            <Route path='/instruments/:instrumentAddress/channels/:channelName' component={SingleChannel} />
                            <Route path='/instruments/:instrumentAddress' component={SingleInstrument} />
                        </Switch>
                    </Layout.Sider>
                    <Layout.Content>
                        <Switch>
                            <Route exact path='/' component={() => null} />
                            <Route path='/instruments/add' component={() => null} />
                            <Route path='/instruments/:instrumentAddress' component={Figure} />
                        </Switch>
                    </Layout.Content>
                </Layout>
            </Router>
        </ApiProvider>
    );
}
