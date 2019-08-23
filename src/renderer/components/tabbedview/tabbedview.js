import React, { Children } from 'react';
import { withRouter } from "react-router";
import { HashRouter as Router, Route, Link, Redirect } from 'react-router-dom';

import './tabbedview.scss';

const TabList = withRouter(({ children, location }) => (
    <div className='handle'>
        <ul className='tabs'>
            {
                Children.map(children, ({ props: { path, name, active }}) => (
                    <Link className={`tab ${location.pathname === path ? 'active' : ''}`} to={path}><li>{name}</li></Link>
                ))
            }
        </ul>
        <button className='minimize'></button>
        <button className='maximize'></button>
        <button className='close'></button>
    </div>
));

export function TabbedView({ children }) {
    
    return (
        <div className='tabbedview'>
            <Router>
                <TabList>
                    { children }
                </TabList>
                <Route exact path='/' component={() => {
                    if (Children.count(children) === 0) {
                        return null;
                    }

                    const path = Children.toArray(children)[0].props.path;

                    return <Redirect to={path} />;
                }} />
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
