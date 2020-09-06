import React from 'react';
import { Menu } from 'antd';

export function Menubar() {
    return (
        <Menu
            mode='horizontal'
            triggerSubMenuAction='click'
        >
            <Menu.SubMenu
                title='File'
            >
                <Menu.Item>
                    Open file...
                </Menu.Item>
            </Menu.SubMenu>
        </Menu>
    );
}
