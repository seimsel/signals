import React from 'react';
import { Layout, Spin, Tabs } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import { useQuery, useMutation } from '@apollo/client';
import { ApiProvider } from '../../api/components/api-provider';
import { Menubar } from './menubar';
import { Sider } from './sider';
import { Content } from './content';
import measurementsQuery from '../queries/measurements.graphql';
import closeMeasurementMutation from '../mutations/close-measurement.graphql'

function Main() {
    const { data, loading } = useQuery(measurementsQuery);
    const [ closeMeasurement ] = useMutation(closeMeasurementMutation);

    return (
        <Spin
            indicator={
                <LoadingOutlined
                    style={{
                        fontSize: '10em'
                    }}
                    spin
                />
            }
            spinning={ loading }
        >
            <Layout
                style={{ height:"100vh" }}
            >
                <Layout.Header
                    style={{ padding: 0 }}
                >
                    { loading ? null : <Menubar window={ data.session.windows[0] } /> }
                </Layout.Header>
                <Tabs
                    type='editable-card'
                    className='full-height'
                    onEdit={ (targetKey, action) => {
                        switch (action) {
                            case 'remove':
                                closeMeasurement({
                                    variables: {
                                        measurementId: targetKey,
                                        windowId: data.session.windows[0].id
                                    }
                                });
                                return;
                            
                            case 'add':
                            default:
                                return;
                        }
                    }}
                    hideAdd
                >
                {
                    loading || data.session.windows[0].measurements.length === 0 ? null :
                    data.session.windows[0].measurements.map(measurement => (
                        <Tabs.TabPane
                            tab={ measurement.name }
                            key={ measurement.id }
                        >
                            <Layout>
                                <Layout.Sider
                                    width={300}
                                    collapsible
                                    collapsedWidth={0}
                                >
                                    { loading ? null : <Sider measurement={ measurement } /> }
                                </Layout.Sider>
                                <Layout.Content>
                                    { loading ? null : <Content measurement={ measurement } /> }
                                </Layout.Content>
                            </Layout>
                        </Tabs.TabPane>
                    ))
                }
                </Tabs>
            </Layout>
        </Spin>
    );
}

export function App() {
    return (
        <ApiProvider>
            <Main />
        </ApiProvider>
    );
}
