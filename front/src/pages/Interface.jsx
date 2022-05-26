import { Layout, Menu, Upload, message, Table, Form, Input, InputNumber, Select, Card, Transfer, Tree, PageHeader, Row, Col, Divider, Button, Space, Modal, Skeleton, Switch, Affix, Popover, Breadcrumb } from 'antd';
import { React, useState, useRef, createRef, forwardRef, useEffect, lazy } from "react";
import { MailOutlined, SettingOutlined, AppstoreOutlined} from '@ant-design/icons';
import Model1 from "../components/Model1";
const { Header, Content, Footer } = Layout;


const menus = [
    {
        key: 0,
        label: '模型一',
        component: <Model1></Model1>
    },
    // {
    //     key: 1,
    //     label: '模型二'
    // },
    // {
    //     key: 2,
    //     label: '模型三'
    // },
];

const Interface = () => {

    
    const [selectedMenuItem, setSelectedMenuItem] = useState([]);

    return (<div style={{
        backgroundColor: "#f0f2f5"
    }}>
    <Layout>
    <Header
      style={{
        position: 'fixed',
        zIndex: 1,
        width: '100%',
        backgroundColor: 'white',
      }}
    >
      <div className="logo" />
      <Menu
        theme="light"
        mode="horizontal"
        defaultSelectedKeys={['2']}
        selectedKeys={selectedMenuItem}
        items={menus}
        onSelect={(value) => {
            setSelectedMenuItem([value.key]);
        }}
      />
    </Header>
    
    <Content
        className="site-layout"
        style={{
            padding: '5px 5px',
            marginTop: 64
          }}
    >

        {
            selectedMenuItem.length > 0 ? <Card title={menus[selectedMenuItem[0]].label}>
                {menus[selectedMenuItem[0]].component}
            </Card> : <Card>
                欢迎使用新冠预测系统
            </Card>
        }

    </Content>

  </Layout>



    </div>
);
}


export default Interface;