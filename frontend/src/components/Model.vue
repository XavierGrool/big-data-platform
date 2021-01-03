<template>
<a-layout style="padding: 0 24px 24px">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Workspace</a-breadcrumb-item>
        <a-breadcrumb-item>Projects</a-breadcrumb-item>
        <a-breadcrumb-item>{{ project_name }}</a-breadcrumb-item>
        <a-breadcrumb-item>Model</a-breadcrumb-item>
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
                <a @click="() => modifyDataset(record.key)">变更</a>
                <a-divider type="vertical" />
                <a-popconfirm
                    title="确认要删除此数据集吗？"
                    ok-text="确定"
                    cancel-text="取消"
                    @confirm="() => deleteOne(record.key)"
                >
                    <a>删除</a>
                </a-popconfirm>
            </span>
        </a-table>
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
            table_loading: false
        }
    },
    beforeCreate() {
        console.log(this.$route.params.project_id)
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
    }
}
</script>
