import React, { Children, createContext } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { NavTab } from 'react-router-tabs';

import './tabbedview.scss';

export const TabsContext = createContext();

export function Tab({ path, children }) {
    return <Route key={path} path={path}>{ children }</Route>;
}

export function TabbedView({ children }) {
    return (
        <div className='tabbedview'>
            <Router>
                <div className='header'>
                    <ul className='tabs'>
                    {
                        Children.map(children, child => <NavTab className='tab' key={child.props.path} to={child.props.path}><li>{child.props.name}</li></NavTab>)
                    }
                    </ul>
                </div>

                <div className='content'>
                <Switch>
                    { children }
                </Switch>
                </div>
            </Router>
        </div>
    );
}
