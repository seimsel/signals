import React, { Children } from 'react';
import { HashRouter as Router, Route, Link, Redirect } from 'react-router-dom';

export function TabbedView({ children }) {
    return (
        <div>
            <Router>
                <ul>
                    {
                        Children.map(children, ({ props: { path, name } }) => (
                            <li><Link to={path}>{name}</Link></li>
                        ))
                    }
                </ul>
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
