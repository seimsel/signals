import React, { useState, useEffect } from 'react';
import './app.scss';

import { TabbedView } from '../tabbedview';
import { MeasurementView } from '../measurementview';

function App() {
    const [tabs, setTabs] = useState([]);

    useEffect(() => {
        if (tabs.length === 0) {
            setTabs([{ path: '/new', name: 'New' }])
        }
    }, [tabs]);

    return (
        <TabbedView>
            {
                tabs.map(tab => (
                    <MeasurementView key={tab.path} path={tab.path} name={tab.name} />
                ))
            }
        </TabbedView>
    );
}

export default App;
