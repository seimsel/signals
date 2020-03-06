import React from 'react';
import { ApiProvider } from '../../api/components/api-provider';
import { ChannelList } from '../../channels/components/channel-list';
import { Figure } from '../../figure/components/figure';

const address = 'scope1.demo';

export function App() {
    return (
        <ApiProvider>
            <aside>
                <ChannelList address={address}/>
            </aside>
            <main>
                <Figure address={address} />
            </main>
        </ApiProvider>
    );
}
