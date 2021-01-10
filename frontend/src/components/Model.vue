<template>
<a-layout style="padding: 0 24px 24px">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>工作台</a-breadcrumb-item>
        <a-breadcrumb-item>项目空间</a-breadcrumb-item>
        <a-breadcrumb-item>{{ project_name }}</a-breadcrumb-item>
        <a-breadcrumb-item>模型管理</a-breadcrumb-item>
    </a-breadcrumb>
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        <a-space style="margin-bottom: 12px">
            <a-button @click="addModel"><a-icon type="file-add" />添加模型</a-button>
            <a-button @click="deleteSelected" type="danger"><a-icon type="delete" />删除</a-button>
        </a-space>
        <a-table
            :columns="columns"
            :data-source="data"
            :pagination="pagination"
            :row-selection="rowSelection"
            :loading="table_loading"
            @change="handleTableChange"
        >
            <span slot="action" slot-scope="record">
                <a @click="() => modifyModel(record.key)">变更</a>
                <a-divider type="vertical" />
                <a-popconfirm
                    title="确认要删除此模型吗？"
                    ok-text="确定"
                    cancel-text="取消"
                    @confirm="() => deleteOne(record.key)"
                >
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
        <a-modal
            title="模型变更"
            :visible="modify_model_modal"
            :footer="null"
            @cancel="closeModifyModelModal"
        >
            <a-form
                :form="modify_model_form"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 12 }"
                @submit="submitModification"
            >
                <a-form-item label="模型名称">
                    <a-input :value="tmp_name" />
                </a-form-item>
                <a-form-item label="模型描述">
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
</template>

<script>
const columns = [
    {
        title: '模型名称',
        dataIndex: 'name',
        width: "20%",
    },
    {
        title: '描述',
        dataIndex: 'description',
    },
    {
        title: '操作',
        scopedSlots: { customRender: 'action' },
        width: "20%"
    },
];

export default {
    name: "Model",
    data() {
        return {
            project_name: "",
            columns: columns,
            data: [],
            pagination: {
                current: 1,
                defaultPageSize: 5,
                total: 1
            },
            rowSelection: {
                onChange: (selectedRowKeys) => {
                    this.selected_row_keys = selectedRowKeys;
                    console.log("selected_row_keys")
                    console.log(this.selected_row_keys)
                }
            },
            table_loading: false,
            modify_model_modal: false,
            modify_model_form: this.$form.createForm(this, { name: 'modify_model' }),
            tmp_name: "",
            tmp_description: "",
        }
    },
    created() {
        console.log(this.$route.params.project_id)
        this.table_loading = true;

        // 获取项目名称
        this.$axios({
            method: 'post',
            url: '/project/get-name/',
            data: {
                "id": Number(this.$route.params.project_id)
            }
        }).then((response) => {
            console.log(response.data);
            this.project_name = response.data.name;
        })

        // 获取所有模型
        this.$axios({
            method: 'post',
            url: '/model/get-all/',
            data: {
              "project_id": Number(this.$route.params.project_id),
              "num": 5,
              "start": 1
            }
        }).then((response) => {
            console.log(response.data);
            this.data = response.data.models;
            this.pagination.total = response.data.total;
            this.table_loading = false;
        })
    },
    methods: {
        // 点击添加模型
        addModel() {
            this.$router.replace("/dashboard/workspace/project/" + this.$route.params.project_id + "/model/add")
        },

        // 删除选中的项目
        deleteSelected() {
            console.log("删除一堆");
            // TODO
        },

        // 当分页发生变化时
        handleTableChange(pagination) {
            console.log("分页发生了变化！")
            console.log(pagination);
            this.pagination.current = pagination.current;
            // this.$axios({
            //     method: 'post',
            //     url: '/project/get-all/',
            //     data: {
            //         "username": this.$cookies.get("username"),
            //         "num": 5,
            //         "start": (pagination.current - 1) * pagination.pageSize + 1
            //     }
            // }).then((response) => {
            //     console.log(response.data);
            //     this.data = response.data.projects;
            //     this.pagination.total = response.data.total;
            // })
        },

        // 删除一个模型
        deleteOne(key) {
            console.log("要删除的模型是:");
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

        // 点击修改模型
        modifyModel(key) {
            console.log("修改模型");
            console.log(this.data[Number(key) - 1].name);
            console.log(this.data[Number(key) - 1].description);
            this.tmp_name = this.data[Number(key) - 1].name;
            this.tmp_description = this.data[Number(key) - 1].description;
            this.modify_model_modal = true;
        },

        // 关闭修改模型对话框
        closeModifyModelModal() {
            this.modify_model_modal = false;
        },

        // 提交模型变更
        submitModification(e) {
            e.preventDefault();
            this.modify_model_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                    // TODO
                }
            })
        },
    }
}
</script>
