import { Layout, Tree } from 'antd';

const { Sider, Content } = Layout;

export default function Home() {
    const data = [];
    const treeData = data.map(item => item);

    return (
        <Layout>
            <Sider>
                <Tree
                    treeData={treeData}
                />
            </Sider>
            <Content>
                Ho
            </Content>
        </Layout>
    );
}
