import React, { useContext, useEffect } from 'react';
import './app.scss'; 

import { TabbedView } from '../tabbedview/tabbedview';
import { MainComponent } from '../tabbedview/maincomponent';

export function App() {
    return (
        <TabbedView mainComponent={MainComponent} />
    );
}
