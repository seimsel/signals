import React, { Children } from 'react';
import { withRouter } from "react-router";
import { HashRouter as Router, Route, Link, Redirect } from 'react-router-dom';

import './tabbedview.scss';

const TabList = withRouter(({ children, location, onNew }) => (
    <div className='handle'>
        <ul className='tabs'>
            {
                Children.map(children, ({ props: { path, name, active }}) => (
                    <Link className={`tab ${location.pathname === path ? 'active' : ''}`} to={path}><li>{name}</li></Link>
                ))
            }
            <button className={'new'} onClick={onNew}></button>
        </ul>
        <button className='minimize' onClick={() => {window.minimize()}}></button>
        <button className='maximize' onClick={() => {
            window.isMaximized() ? window.restore() : window.maximize();
        }}></button>
        <button className='close' onClick={() => {window.close()}}></button>
    </div>
));

export function TabbedView({ children, onNew }) {
    
    return (
        <div className='tabbedview'>
            <Router>
                <TabList onNew={onNew}>
                    { children }
                </TabList>
                {
                    Children.map(children, child => {
                        const { props: { path } } = child;

                        return (
                            <Route path={path} component={() => (child)} />
                        )
                    })
                }
            </Router>
        </div>

    );
}
