import React, { useState, useEffect } from 'react';
import './app.scss';

import { TabbedView } from '../tabbedview';
import { Dropzone } from '../dropzone';
import { MeasurementView } from '../measurementview';
import { v4 } from 'uuid';

function App() {
    const [tabs, setTabs] = useState([]);

    useEffect(() => {
        if (tabs.length === 0) {
            const path = `/new://${v4()}`;
            setTabs([{path, name: 'New'}])
            window.location.href = `#${path}`;
        }
    }, [tabs]);

    return (
        <TabbedView onNew={() => {
            const path = `/new://${v4()}`;
            setTabs([...tabs, {path, name: 'New'}])
            window.location.href = `#${path}`;
        }}>
            {
                tabs.map(tab => {
                    if (tab.path.split('/')[1] === 'new:') {
                        return <div key={tab.path} path={tab.path} name={tab.name} className='dropzone-page'><Dropzone onChange={({target}) => {
                            const file = target.files[0];
                            const path = `/file://${file.path}`;

                            setTabs([...tabs.filter(t => t.path !== tab.path), {
                                name: file.name,
                                path
                            }]);

                            window.location.href = `#${path}`;
                        }} /></div>;
                    } else {
                        console.log(tab.path)
                        return <MeasurementView key={tab.path} path={tab.path} name={tab.name} />;
                    }
                })
            }
        </TabbedView>
    );
}

export default App;
