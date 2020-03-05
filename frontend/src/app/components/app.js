import React from 'react';
import { ApiProvider } from '../../api/components/api-provider';
import { FunctionList } from '../../functions/components/function-list';
import { Figure } from '../../figure/components/figure';

const address = '10.1.11.79';

export function App() {
    return (
        <ApiProvider>
            <aside>
                {/* <FunctionList address={address}/> */}
            </aside>
            <main>
                <Figure address={address} />
            </main>
        </ApiProvider>
    );
}
