<template>
<a-layout>
    <a-layout-sider width="200" style="background: #fff">
    <a-menu
        mode="inline"
        :default-selected-keys="['2']"
        :style="{ height: '100%', borderRight: 0 }"
    >
        <a-menu-item key="1" @click="clickProjects">
            <a-icon type="project" />项目空间
        </a-menu-item>
        <a-menu-item key="2" @click="clickUsers">
            <a-icon type="user" />用户管理
        </a-menu-item>
    </a-menu>
    </a-layout-sider>
    <a-layout style="padding: 0 24px 24px">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Home</a-breadcrumb-item>
        <a-breadcrumb-item>List</a-breadcrumb-item>
        <a-breadcrumb-item>App</a-breadcrumb-item>
    </a-breadcrumb>
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        <a-space style="margin-bottom: 12px">
            <a-button @click="addUser"><a-icon type="user-add" />添加</a-button>
            <a-button @click="deleteSelected" type="danger"><a-icon type="user-delete" />删除</a-button>
        </a-space>
        <a-modal
            title="添加用户"
            :visible="add_user_modal"
            :footer="null"
            @cancel="closeAddUserModal"
        >
            <a-form :form="add_user_form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }" @submit="submitAddUser">
                <a-form-item label="用户名">
                    <a-input
                        v-decorator="['username', { rules: [{ required: true, message: '用户名不得为空!' }] }]"
                    />
                </a-form-item>
                <a-form-item label="密码">
                    <a-input
                        v-decorator="['passwd', { rules: [{ required: true, message: '密码不得为空!' }] }]"
                        type="password"
                    />
                </a-form-item>
                <a-form-item label="确认密码">
                    <a-input
                        v-decorator="['confirm_passwd', { rules: [{ required: true, message: '确认密码不得为空!' }] }]"
                        type="password"
                    />
                </a-form-item>
                <a-form-item label="用户权限">
                    <a-tree-select
                        v-decorator="['permission', { rules: [{ required: true, message: '请分配用户权限!' }] }]"
                        style="width: 100%"
                        :tree-data="treeData"
                        tree-checkable
                        :show-checked-strategy="SHOW_PARENT"
                    />
                </a-form-item>
                <a-form-item :wrapper-col="{ span: 12, offset: 5 }">
                    <a-button type="primary" html-type="submit">
                        提交
                    </a-button>
                </a-form-item>
            </a-form>
        </a-modal>
        <a-table
            :columns="columns"
            :data-source="data"
            :pagination="pagination"
            :row-selection="rowSelection"
            @change="handleTableChange"
        >
            <span slot="customUsernameTitle"><a-icon type="smile-o" /> 用户名</span>
            <span slot="tags" slot-scope="tags">
                <a-tag
                    v-for="tag in tags"
                    :key="tag"
                    :color="tag === 'loser' ? 'volcano' : tag.length > 5 ? 'geekblue' : 'green'"
                >
                    {{ tag.toUpperCase() }}
                </a-tag>
            </span>
            <span slot="action" slot-scope="record">
                <a @click="() => changePermission(record.key)">修改</a>
                <a-divider type="vertical" />
                <a-popconfirm
                    title="确认要删除此账户吗？"
                    ok-text="确定"
                    cancel-text="取消"
                    @confirm="() => deleteOne(record.key)"
                >
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
        <a-modal
            title="修改账户权限"
            :visible="change_permission_modal"
            :footer="null"
            @cancel="closeChangePermissionModal"
        >
            <a-form
                :form="change_permission_form"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 12 }"
                @submit="submitPermission"
            >
                <a-form-item label="用户名">
                    <a-input disabled :value="tmp_username"/>
                </a-form-item>
                <a-form-item label="用户权限">
                    <a-tree-select
                        v-decorator="['permission', { rules: [{ required: true, message: '请分配用户权限!' }] }]"
                        style="width: 100%"
                        :tree-data="treeData"
                        tree-checkable
                        :show-checked-strategy="SHOW_PARENT"
                    />
                </a-form-item>
                <a-form-item :wrapper-col="{ span: 12, offset: 5 }">
                    <a-button type="primary" html-type="submit">
                        提交
                    </a-button>
                </a-form-item>
            </a-form>
        </a-modal>
    </a-layout-content>
    </a-layout>
</a-layout>
</template>

<script>
import { TreeSelect } from 'ant-design-vue';
const SHOW_PARENT = TreeSelect.SHOW_PARENT;

const treeData = [
  {
    title: 'Node1',
    value: '0-0',
    key: '0-0',
    children: [
      {
        title: 'Child Node1',
        value: '0-0-0',
        key: '0-0-0',
      },
    ],
  },
  {
    title: 'Node2',
    value: '0-1',
    key: '0-1',
    children: [
      {
        title: 'Child Node3',
        value: '0-1-0',
        key: '0-1-0',
        disabled: true,
      },
      {
        title: 'Child Node4',
        value: '0-1-1',
        key: '0-1-1',
      },
      {
        title: 'Child Node5',
        value: '0-1-2',
        key: '0-1-2',
      },
    ],
  },
];

const columns = [
  {
    dataIndex: 'name',
    slots: { title: 'customUsernameTitle' },
  },
  {
    title: '权限',
    dataIndex: 'permission',
    scopedSlots: { customRender: 'tags' },
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' },
  },
];

export default {
    name: "Users",
    data() {
        return {
            treeData,
            SHOW_PARENT,
            add_user_form: this.$form.createForm(this, { name: 'add_user' }),
            change_permission_form: this.$form.createForm(this, { name: 'change_permission' }),
            add_user_modal: false,
            change_permission_modal: false,
            tmp_username: "",
            data: [],
            columns,
            pagination: {
                current: 1,
                defaultPageSize: 5,
                total: 1
            },
            rowSelection: {
                onChange: (selectedRowKeys) => {
                    this.selected_row_keys = selectedRowKeys;
                }
            },
            selected_row_keys: {}
        }
    },
    beforeCreate() {
        this.$axios({
            method: 'post',
            url: '/user/get-all/',
            data: {
              "num": 5,
              "start": 1
            }
        }).then((response) => {
            console.log(response.data);
            this.data = response.data.users;
            this.pagination.total = response.data.total;
        })
    },
    methods: {
        // 点击项目空间
        clickProjects(e) {
            console.log(e);
            this.$router.push("/dashboard/workspace/projects")
        },

        // 点击用户管理（其实没什么用
        clickUsers(e) {
            console.log(e);
        },

        // 点击添加用户
        addUser() {
            console.log("添加用户");
            this.add_user_modal = true;
        },

        // 关闭添加用户对话框
        closeAddUserModal() {
            this.add_user_modal = false;
        },

        // 提交添加用户
        submitAddUser(e) {
            e.preventDefault();
            this.add_user_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                    // 先判断一下两次密码一不一致
                    // 如果如果不一致，弹警告
                    // 一致的话，调用 /user/add 接口 (POST)
                    // 发送 username, passwd, permission
                    if (values.passwd != values.confirm_passwd) {
                        this.$message.error('两次密码输入不一致！');
                    } else {
                        this.$axios({
                            method: 'post',
                            url: '/user/add/',
                            data: {
                                "username": values.username,
                                "passwd": values.passwd,
                                "permission": 15
                            }
                        }).then((response) => {
                            console.log(response.data);
                            // 如果状态码 status 为 0，说明添加用户失败，弹警告
                            // 如果 status 为 1，说明添加用户成功
                            // 提示添加成功，并刷新路由
                            if (response.data.status == 0) {
                                this.$message.error('添加用户失败！');
                            } else if (response.data.status == 1) {
                                this.$message.success('添加成功！');
                                this.$router.go(0);
                            } else {
                                this.$message.error('非法状态！');
                            }

                        })
                    }
                }
            });
        },

        // 当分页发生变化时
        handleTableChange(pagination) {
            console.log("分页发生了变化！")
            console.log(pagination);
            this.pagination.current = pagination.current;
            this.$axios({
                method: 'post',
                url: '/user/get-all/',
                data: {
                    "num": 5,
                    "start": (pagination.current - 1) * pagination.pageSize + 1
                }
            }).then((response) => {
                console.log(response.data);
                this.data = response.data.users;
                this.pagination.total = response.data.total;
            })
        },

        // 删除一个账户
        deleteOne(key) {
            console.log("要删除的账户是:");
            console.log(key);
            this.$axios({
                method: 'post',
                url: '/user/delete/one/',
                data: {"id": this.data[Number(key) - 1].id}
            }).then((response) => {
                console.log(response.data);
                if (response.data.status == 0) {
                    this.$message.error('删除用户失败！');
                } else if (response.data.status == 1) {
                    this.$message.success('删除用户成功！');
                    this.$router.go(0);
                } else {
                    this.$message.error('非法状态！');
                }
            })
        },

        // 删除选中的账户
        deleteSelected() {
            console.log("删除一堆");
            console.log(this.selected_row_keys);
            var ids = new Array();
            for (var i = 0; i < this.selected_row_keys.length; i++) {
                ids[i] = this.data[Number(this.selected_row_keys[i]) - 1].id
            }
            this.$axios({
                method: 'post',
                url: '/user/delete/some/',
                data: {ids: ids}
            }).then((response) => {
                console.log(response.data);
                if (response.data.status == 0) {
                    this.$message.error('删除用户失败！');
                } else if (response.data.status == 1) {
                    this.$message.success('删除用户成功！');
                    this.$router.go(0);
                } else {
                    this.$message.error('非法状态！');
                }
            })
        },

        // 点击修改用户权限
        changePermission(key) {
            console.log("修改用户权限");
            console.log(this.data[Number(key) - 1].name);
            console.log(this.data[Number(key) - 1].permission);
            this.tmp_username = this.data[Number(key) - 1].name;
            this.change_permission_modal = true;
        },

        // 关闭修改用户权限对话框
        closeChangePermissionModal() {
            this.change_permission_modal = false;
        },

        // 提交权限变更
        submitPermission(e) {
            e.preventDefault();
            this.change_permission_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                }
            })
        }
    }
}
</script>
