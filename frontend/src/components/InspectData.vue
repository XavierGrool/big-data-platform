<template>
<a-layout>
    <a-layout-sider width="200" style="background: #fff">
    <div style="height:64px;padding-top:20px;">
        <a @click="returnToDatasets" style="fontSize:24px;margin-left:88px">
            <a-icon type="left" />
        </a>
    </div>
    </a-layout-sider>
    <a-layout style="padding: 0 24px 24px">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>Workspace</a-breadcrumb-item>
            <a-breadcrumb-item>Projects</a-breadcrumb-item>
            <a-breadcrumb-item>{{ project_name }}</a-breadcrumb-item>
            <a-breadcrumb-item>Dataset</a-breadcrumb-item>
            <a-breadcrumb-item>{{ dataset_name }}</a-breadcrumb-item>
        </a-breadcrumb>
        <a-layout-content
            :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
        >
            <a-table
                :columns="columns"
                :data-source="data"
                :pagination="pagination"
                :loading="table_loading"
                @change="handleTableChange"
            >
            </a-table>
        </a-layout-content>
    </a-layout>
</a-layout>
</template>

<script>
const test_columns = [
    {
        title: '数据集名称',
        dataIndex: 'name',
    },
    {
        title: '描述',
        dataIndex: 'description',
    },
];

const test_data = [
    {
        id: 1,
        key: '1',
        name: 'Iris',
        description: 'class ~ sepal length + sepal width + petal length + petal width'
    },
    {
        id: 2,
        key: '2',
        name: 'Caesarian',
        description: 'caesarian ~ age + delivery number + delivery time + blood of pressure + heart problem'
    },
];

export default {
    name: "InspectData",
    data() {
        return {
            project_name: "",
            dataset_name: "",
            table_loading: false,
            columns: [],
            data: [],
            pagination: {
                current: 1,
                defaultPageSize: 20,
                total: 1
            },
        }
    },
    created() {
        console.log(this.$route.path);
        console.log(this.$route.params.project_id)
        console.log(this.$route.params.dataset_id)

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
        });

        // 获取数据集名称
        this.$axios({
            method: 'post',
            url: '/dataset/get-name/',
            data: {
                "id": Number(this.$route.params.dataset_id)
            }
        }).then((response) => {
            console.log(response.data);
            this.dataset_name = response.data.name;
        });

        // 获取数据
        this.$axios({
            method: 'post',
            url: '/dataset/get-data/',
            data: {
              "id": Number(this.$route.params.dataset_id),
              "num": 20,
              "start": 1
            }
        }).then((response) => {
            console.log(response.data);
            this.data = response.data.data;
            this.columns = response.data.columns;
            this.pagination.total = response.data.total;
            this.table_loading = false;
        })
    },
    methods: {
        // 返回数据集
        returnToDatasets() {
            var path = this.$route.path;
            this.$router.push(path.slice(0, path.lastIndexOf("/")))
        },

        // 当分页发生变化时
        handleTableChange(pagination) {
            console.log("分页发生了变化！")
            console.log(pagination);
            this.table_loading = true;
            this.pagination.current = pagination.current;
            this.$axios({
                method: 'post',
                url: '/dataset/get-data/',
                data: {
                    "id": Number(this.$route.params.dataset_id),
                    "num": 20,
                    "start": (pagination.current - 1) * pagination.pageSize + 1
                }
            }).then((response) => {
                console.log(response.data);
                this.data = response.data.data;
                this.columns = response.data.columns;
                this.pagination.total = response.data.total;
                this.table_loading = false;
            })
        },
    }
}
</script>
