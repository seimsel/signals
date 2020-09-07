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
                        const input = document.createElement('input');
                        input.type = 'file';

                        input.onchange = event => {
                            console.log(event);
                            openFiles({
                                variables: {
                                    urls: [
                                        JSON.stringify(event)
                                    ],
                                    windowId: window.id
                                }
                            });
                        }

                        input.click();
                    }}
                >
                    Open file...
                </Menu.Item>
            </Menu.SubMenu>
        </Menu>
    );
}
