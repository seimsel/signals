import React, { useState, createContext } from 'react';
import { withRouter } from "react-router";
import { HashRouter as Router, Route, Switch } from 'react-router-dom';
import { NavTab } from 'react-router-tabs';

import './tabbedview.scss';

export const TabsContext = createContext();

export function TabbedView({ mainComponent }) {
    const [tabs, setTabs] = useState([]);

    return (
        <div className='tabbedview'>
            <TabsContext.Provider value={[tabs, setTabs]}>
                <Router>
                    <div className='header'>
                        <ul className='tabs'>
                        {
                            tabs.map(tab => <NavTab className='tab' key={tab.path} to={tab.path}><li>{tab.name}</li></NavTab>)
                        }
                        </ul>
                    </div>

                    <div className='content'>
                    <Switch>
                        {
                            tabs.map(tab => <Route key={tab.path} path={tab.path} component={withRouter(tab.component)} />)
                        }
                        <Route path='/' component={withRouter(mainComponent)} />
                    </Switch>
                    </div>
                </Router>
            </TabsContext.Provider>
        </div>
    );
}
