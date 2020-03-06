import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Switch, Route } from 'react-router';
import { ApiProvider } from '../../api/components/api-provider';
import { ChannelList } from '../../channels/components/channel-list';
import { SingleChannel } from '../../channels/components/single-channel';
import { Figure } from '../../figure/components/figure';

const address = 'scope1.demo';

export function App() {
    return (
        <ApiProvider>
            <Router>
                <aside>
                    <Switch>
                        <Route exact path='/' component={() => <ChannelList address={address} />} />
                        <Route path='/channels/:name' component={SingleChannel} />
                    </Switch>
                </aside>
                <main>
                    <Figure address={address} />
                </main>
            </Router>
        </ApiProvider>
    );
}
