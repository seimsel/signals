import React, { useContext, useEffect } from 'react';
import { useMutation } from '@apollo/client';
import { Menu } from 'antd';
import { QtContext } from '../../qt/contexts/qt-context';
import openFilesMutation from '../mutations/open-files.graphql';

export function Menubar({ window }) {
    const [openFiles] = useMutation(openFilesMutation);
    const python = useContext(QtContext);

    useEffect(() => {
        if (!python) {
            return;
        }

        python.fileNamesChanged.connect(fileNames => {          
            openFiles({
                variables: {
                    urls: fileNames.map(fileName => `file://${encodeURIComponent(fileName)}`),
                    windowId: window.id
                }
            });
        });
    }, [python]);

    return (
        <Menu
            mode='horizontal'
            triggerSubMenuAction='click'
        >
            <Menu.SubMenu
                title='File'
            >
                {
                    python ?
                    <Menu.Item
                        onClick={() => {
                            python.getOpenFileNames();
                        }}
                    >
                        Open file...
                    </Menu.Item>
                    :
                    null
                }
            </Menu.SubMenu>
        </Menu>
    );
}
