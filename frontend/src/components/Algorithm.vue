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
        <a-breadcrumb-item>算法管理</a-breadcrumb-item>
    </a-breadcrumb>
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        <a-space style="margin-bottom: 12px">
            <a-button @click="addAlgorithm"><a-icon type="file-add" />添加</a-button>
            <a-button @click="deleteSelected" type="danger"><a-icon type="delete" />删除</a-button>
        </a-space>
        <a-modal
            title="添加算法"
            :visible="add_algorithm_modal"
            :footer="null"
            @cancel="closeAddAlgorithmModal"
        >
            <a-form
                :form="add_algorithm_form"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 12 }"
                @submit="submitAddAlgorithm"
            >
                <a-form-item label="算法名称">
                    <a-input
                        v-decorator="['al_name', { rules: [{ required: true, message: '算法名称不得为空!' }] }]"
                    />
                </a-form-item>
                <a-form-item label="描述">
                    <a-textarea placeholder="选填" v-decorator="['description']" :rows="4" />
                </a-form-item>
                <a-form-item label="接口">
                    <a-input
                        v-decorator="['interface', { rules: [{ required: true, message: '接口不得为空!' }] }]"
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
            :pagination="false"
            :row-selection="rowSelection"
        >
            <span slot="action" slot-scope="record">
                <a @click="() => modifyAlgorithm(record.key)">变更</a>
                <a-divider type="vertical" />
                <a-popconfirm
                    title="确认要删除此算法吗？"
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
</a-layout>
</template>

<script>
const columns = [
    {
        title: '算法名称',
        dataIndex: 'name',
        width: "30%",
    },
    {
        title: '算法描述',
        dataIndex: 'description',
    },
    {
        title: '操作',
        scopedSlots: { customRender: 'action' },
        width: "20%"
    },
];

const test_data = [
    {
        name: 'Logistic Regression',
        description: '逻辑回归分类',
        key: '1',
    },
    {
        name: 'Decision Tree Classifier',
        description: '决策树分类',
        key: '2',
    },
    {
        name: 'Random Forest Classifier',
        description: '随机森林分类',
        key: '3',
    },
    {
        name: 'Gradient-boosted Tree Classifier',
        description: '梯度提升树分类',
        key: '4',
    },
    {
        name: 'Naive Bayes',
        description: '朴素贝叶斯分类',
        key: '5',
    },
    {
        name: 'Linear Support Vector Machine',
        description: '支持向量机分类',
        key: '6',
    },
    {
        name: 'Linear Regression',
        description: '线性回归',
        key: '7',
    },
    {
        name: 'Random Forest Regression',
        description: '随机森林回归',
        key: '8',
    },
    {
        name: 'Gradient-boosted Tree Regression',
        description: '梯度提升树回归',
        key: '9',
    },
];

export default {
    name: "Algorithm",
    data() {
        return {
            data: test_data,
            columns,
            add_algorithm_modal: false,
            add_algorithm_form: this.$form.createForm(this, { name: 'add_algorithm' }),
            selected_row_keys: {},
            rowSelection: {
                onChange: (selectedRowKeys) => {
                    this.selected_row_keys = selectedRowKeys;
                }
            },
        }
    },
    created() {

    },
    methods: {
        // 点击项目空间
        clickProjects(e) {
            console.log(e);
            this.$router.push("/dashboard/workspace/projects")
        },

        // 点击算法管理（其实没什么用
        clickAlgorithm(e) {
            console.log(e);
        },

        // 点击用户
        clickUsers(e) {
            console.log(e);
            this.$router.push("/dashboard/workspace/users")
        },

        // 点击添加算法
        addAlgorithm() {
            console.log("添加算法");
            this.add_algorithm_modal = true;
        },

        // 关闭添加算法对话框
        closeAddAlgorithmModal() {
            this.add_algorithm_modal = false;
        },

        // 删除选中的项目
        deleteSelected() {
            console.log("删除一堆");
            // TODO
        },

        // 提交添加算法
        submitAddAlgorithm(e) {
            e.preventDefault();
            this.add_algorithm_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                }
            })
        },

        // 点击修改算法
        modifyAlgorithm() {
            console.log("修改算法");
            // console.log(this.data[Number(key) - 1].name);
            // console.log(this.data[Number(key) - 1].description);
            // this.tmp_name = this.data[Number(key) - 1].name;
            // this.tmp_description = this.data[Number(key) - 1].description;
            // this.modify_project_modal = true;
        },

        // 删除一个算法
        deleteOne(key) {
            console.log("要删除的算法是:");
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
    }
}
</script>
