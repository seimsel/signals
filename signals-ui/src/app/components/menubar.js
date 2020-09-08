import React from 'react';
import { useMutation } from '@apollo/client';
import { Menu } from 'antd';
import openFilesMutation from '../mutations/open-files.graphql';

export function Menubar({ window }) {
    const [openFiles] = useMutation(openFilesMutation);

    return (
        <Menu
            mode='horizontal'
            triggerSubMenuAction='click'
        >
            <Menu.SubMenu
                title='File'
            >
                <Menu.Item
                    onClick={() => {
                        openFileDialog(files => console.log(files));
                    }}
                >
                    Open file...
                </Menu.Item>
            </Menu.SubMenu>
        </Menu>
    );
}
