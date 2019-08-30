import { useEffect, useContext } from 'react';

import { MeasurementView } from '../measurementview/measurementview';
import { TabsContext } from './tabbedview';
import { WelcomeComponent } from './welcomecomponent';
import { filename, to_unix_path } from '../../util/pathutils';

export function MainComponent({ location, history }) {
    const [tabs, setTabs] = useContext(TabsContext);

    useEffect(() => {
        if (location.pathname === '/') {
            if (tabs[0]) {
                history.push(tabs[0].path);
            } else {
                history.push('/welcome');
            }
        } else {
            if (location.pathname === '/welcome') {
                setTabs([{
                    name: 'Welcome',
                    path: '/welcome',
                    component: WelcomeComponent
                }])
            } else {
                setTabs([...tabs, {
                    name: filename(location.pathname),
                    path: to_unix_path(location.pathname),
                    component: MeasurementView
                }])
            }
        }

    }, [location.pathname]);

    return null;
}
