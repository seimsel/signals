import React, { useContext, useEffect } from 'react';
import { useMutation } from '@apollo/client';
import { Menu } from 'antd';
import { QtContext } from '../../qt/contexts/qt-context';
import openFilesMutation from '../mutations/open-files.graphql';

export function Menubar({ window }) {
    const [openFiles] = useMutation(openFilesMutation);
    const python = useContext(QtContext);

    useEffect(() => {
        python.fileNamesChanged.connect(fileNames => openFiles({
                variables: {
                    urls: fileNames.map(fileName => `file://${encodeURIComponent(fileName)}`),
                    windowId: window.id
                }
            }));
    }, []);

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
                        console.error('hi');
                        const files = python.getOpenFileNames();
                        console.error(files);

                        // files => openFiles({
                        //     variables: {
                        //         urls: files.map(file => `file://${encodeURIComponent(file)}`),
                        //         windowId: window.id
                        //     }
                        // })
                    }}
                >
                    Open file...
                </Menu.Item>
            </Menu.SubMenu>
        </Menu>
    );
}
