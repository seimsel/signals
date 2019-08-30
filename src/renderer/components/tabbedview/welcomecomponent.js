import React, { useContext } from 'react';
import { TabsContext } from './tabbedview';
import { MeasurementView } from '../measurementview/measurementview';
import { Dropzone } from './../dropzone/dropzone';
import { distinct } from '../../util/arrayutils';
import { to_unix_path } from '../../util/pathutils';

export function WelcomeComponent({ history }) {
    const [tabs, setTabs] = useContext(TabsContext);

    return (
        <Dropzone onChange={({ target }) => {
            let newTabs = [];

            for (let file of target.files) {
                newTabs.push({
                    name: file.name,
                    path: to_unix_path(`/file://${file.path || file.name}`),
                    component: MeasurementView
                });
            }

            if (newTabs.length === 0) {
                return;
            }

            setTabs(distinct([...tabs, ...newTabs], 'path'));
            history.push(newTabs[0].path);
        }} />
    );
}
