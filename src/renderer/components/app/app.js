import React, { useState, useEffect } from 'react';
import './app.scss';

import { TabbedView } from '../tabbedview';
import { Dropzone } from '../dropzone';
import { MeasurementView } from '../measurementview';

function App() {
    const [tabs, setTabs] = useState([]);

    useEffect(() => {
        setTabs([
            { name: 'Hello', path: '/hello' },
            { name: 'World', path: '/world' }
        ])
    }, [])

    return (
        <TabbedView>
            {
                tabs.length === 0 ? <Dropzone key='/new' path='/new' name='New' onChange={
                    (event) => {
                        const newTabs = Array.from(event.target.files).map((file) => ({
                            name: file.name,
                            path: file.path
                        }));
                        setTabs([...tabs, ...newTabs]);
                    }
                }/> : tabs.map(tab => (
                    <MeasurementView key={tab.path} path={tab.path} name={tab.name} />
                ))
            }
        </TabbedView>
    );
}

export default App;
