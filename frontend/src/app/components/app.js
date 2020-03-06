import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Switch, Route } from 'react-router';
import { ApiProvider } from '../../api/components/api-provider';
import { SingleInstrument } from '../../instruments/components/single-instrument';
import { SingleChannel } from '../../channels/components/single-channel';
import { SingleParameter } from '../../parameters/components/single-parameter';
import { Figure } from '../../figure/components/figure';

export function App() {
    return (
        <ApiProvider>
            <Router>
                <aside>
                    <Switch>
                        <Route path='/instruments/:instrumentAddress/channels/:channelName/parameters/:parameterName' component={SingleParameter} />
                        <Route path='/instruments/:instrumentAddress/channels/:channelName' component={SingleChannel} />
                        <Route path='/instruments/:instrumentAddress' component={SingleInstrument} />
                    </Switch>
                </aside>
                <main>
                    <Route path='/instruments/:instrumentAddress' component={Figure} />
                </main>
            </Router>
        </ApiProvider>
    );
}
