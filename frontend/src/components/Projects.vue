<template>
<a-layout>
    <a-layout-sider width="200" style="background: #fff">
    <a-menu
        mode="inline"
        :default-selected-keys="['1']"
        :style="{ height: '100%', borderRight: 0 }"
    >
        <a-menu-item key="1" @click="clickProjects">
            <a-icon type="project" />项目空间
        </a-menu-item>
        <a-menu-item key="2" @click="clickAlgorithm">
            <a-icon type="bulb" />算法管理
        </a-menu-item>
        <a-menu-item key="3" @click="clickUsers">
            <a-icon type="user" />用户管理
        </a-menu-item>
    </a-menu>
    </a-layout-sider>
    <a-layout style="padding: 0 24px 24px">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>工作台</a-breadcrumb-item>
        <a-breadcrumb-item>项目空间</a-breadcrumb-item>
    </a-breadcrumb>
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        <a-space style="margin-bottom: 12px">
            <a-button @click="addProject"><a-icon type="file-add" />添加项目</a-button>
            <a-button @click="deleteSelected" type="danger"><a-icon type="delete" />删除</a-button>
        </a-space>
        <a-modal
            title="添加项目"
            :visible="add_project_modal"
            :footer="null"
            @cancel="closeAddProjectModal"
        >
            <a-form
                :form="add_project_form"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 12 }"
                @submit="submitAddProject"
            >
                <a-form-item label="项目名称">
                    <a-input
                        v-decorator="['name', { rules: [{ required: true, message: '项目名不得为空!' }] }]"
                    />
                </a-form-item>
                <a-form-item label="项目描述">
                    <a-textarea placeholder="选填" v-decorator="['description']" :rows="4" />
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
            :loading="table_loading"
            :row-selection="rowSelection"
            @change="handleTableChange"
        >
            <a @click="() => enterProject(record.key)"
                slot="name"
                slot-scope="text, record"
            >{{ text }}</a>
            <span slot="action" slot-scope="record">
                <a @click="() => modifyProject(record.key)">变更</a>
                <a-divider type="vertical" />
                <a-popconfirm
                    title="确认要删除此项目吗？"
                    ok-text="确定"
                    cancel-text="取消"
                    @confirm="() => deleteOne(record.key)"
                >
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
        <a-modal
            title="项目变更"
            :visible="modify_project_modal"
            :footer="null"
            @cancel="closeModifyProjectModal"
        >
            <a-form
                :form="modify_project_form"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 12 }"
                @submit="submitModification"
            >
                <a-form-item label="项目名称">
                    <a-input :value="tmp_name" />
                </a-form-item>
                <a-form-item label="项目描述">
                    <a-textarea :value="tmp_description" :rows="4" />
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
const columns = [
    {
        title: '项目名称',
        dataIndex: 'name',
        scopedSlots: { customRender: 'name' },
        width: "20%",
    },
    {
        title: '项目描述',
        dataIndex: 'description',
    },
    {
        title: '操作',
        scopedSlots: { customRender: 'action' },
        width: "20%"
    },
];

export default {
    name: "Projects",
    data() {
        return {
            add_project_form: this.$form.createForm(this, { name: 'add_project' }),
            modify_project_form: this.$form.createForm(this, { name: 'modify_project' }),
            add_project_modal: false,
            modify_project_modal: false,
            selected_row_keys: {},
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
            data: [],
            columns,
            tmp_name: "",
            tmp_description: "",
            table_loading: false
        }
    },
    created() {
        console.log("现在打开的是项目管理页");
        this.table_loading = true;
        this.$axios({
            method: 'post',
            url: '/project/get-all/',
            data: {
              "username": this.$cookies.get("username"),
              "num": 5,
              "start": 1
            }
        }).then((response) => {
            console.log(response.data);
            this.data = response.data.projects;
            this.pagination.total = response.data.total;
            this.table_loading = false;
        })
    },
    methods: {
        // 点击项目空间（其实没什么用
        clickProjects(e) {
            console.log(e);
        },

        // 点击算法管理
        clickAlgorithm(e) {
            console.log(e);
            this.$router.push("/dashboard/workspace/algorithm")
        },

        // 点击用户管理
        clickUsers(e) {
            console.log(e);
            this.$router.push("/dashboard/workspace/users")
        },

        // 点击添加项目
        addProject() {
            console.log("添加项目");
            this.add_project_modal = true;
        },

        // 删除选中的项目
        deleteSelected() {
            console.log("删除一堆");
            // TODO
        },

        // 关闭添加项目对话框
        closeAddProjectModal() {
            this.add_project_modal = false;
        },

        // 提交添加项目
        submitAddProject(e) {
            e.preventDefault();
            this.add_project_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                    // 先判断一下 description 是不是 undefined/""
                    // 稍微做一下处理就可以给后端发请求了
                    // 接口是 /project/add/ (POST)
                    // 发送 username, name, description
                    if (!values.description) {
                        values.description = "";
                    }
                    this.$axios({
                        method: 'post',
                        url: '/project/add/',
                        data: {
                            "username": this.$cookies.get("username"),
                            "name": values.name,
                            "description": values.description
                        }
                    }).then((response) => {
                        console.log(response.data);
                        // 如果状态码 status 为 0，说明添加项目失败，弹警告
                        // 如果 status 为 1，说明添加项目成功
                        // 提示添加成功，并刷新路由
                        if (response.data.status == 0) {
                            this.$message.error('添加项目失败！');
                        } else if (response.data.status == 1) {
                            this.$message.success('添加成功！');
                            this.$router.go(0);
                        } else {
                            this.$message.error('非法状态！');
                        }
                    })
                }
            })
        },

        // 当分页发生变化时
        handleTableChange(pagination) {
            console.log("分页发生了变化！")
            console.log(pagination);
            this.table_loading = true;
            this.pagination.current = pagination.current;
            this.$axios({
                method: 'post',
                url: '/project/get-all/',
                data: {
                    "username": this.$cookies.get("username"),
                    "num": 5,
                    "start": (pagination.current - 1) * pagination.pageSize + 1
                }
            }).then((response) => {
                console.log(response.data);
                this.data = response.data.projects;
                this.pagination.total = response.data.total;
                this.table_loading = false;
            })
        },

        // 点击修改项目
        modifyProject(key) {
            console.log("修改项目");
            console.log(this.data[Number(key) - 1].name);
            console.log(this.data[Number(key) - 1].description);
            this.tmp_name = this.data[Number(key) - 1].name;
            this.tmp_description = this.data[Number(key) - 1].description;
            this.modify_project_modal = true;
        },

        // 删除一个项目
        deleteOne(key) {
            console.log("要删除的项目是:");
            console.log(key);
            // TODO
            // this.$axios({
            //     method: 'post',
            //     url: '/user/delete/one/',
            //     data: {"id": this.data[Number(key) - 1].id}
            // }).then((response) => {
            //     console.log(response.data);
            //     if (response.data.status == 0) {
            //         this.$message.error('删除用户失败！');
            //     } else if (response.data.status == 1) {
            //         this.$message.success('删除用户成功！');
            //         this.$router.go(0);
            //     } else {
            //         this.$message.error('非法状态！');
            //     }
            // })
        },

        // 关闭修改项目对话框
        closeModifyProjectModal() {
            this.modify_project_modal = false;
        },

        // 提交项目变更
        submitModification(e) {
            e.preventDefault();
            this.modify_project_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                    // TODO
                }
            })
        },

        // 打开项目
        enterProject(key) {
            console.log("项目的 key 是:");
            console.log(key);
            this.$router.push("/dashboard/workspace/project/" + String(this.data[Number(key) - 1].id) + "/dataset")
        }
    }
}
</script>
