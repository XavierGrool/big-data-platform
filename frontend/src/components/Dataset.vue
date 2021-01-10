<template>
<a-layout style="padding: 0 24px 24px">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Workspace</a-breadcrumb-item>
        <a-breadcrumb-item>Projects</a-breadcrumb-item>
        <a-breadcrumb-item>{{ project_name }}</a-breadcrumb-item>
        <a-breadcrumb-item>Dataset</a-breadcrumb-item>
    </a-breadcrumb>
    
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        <a-space style="margin-bottom: 12px">
            <a-button @click="addDataset"><a-icon type="file-add" />添加数据集</a-button>
            <a-button @click="deleteSelected" type="danger"><a-icon type="delete" />删除</a-button>
        </a-space>
        <a-modal
            title="添加数据集"
            width="50%"
            :visible="add_dataset_modal"
            :footer="null"
            @cancel="closeAddDatasetModal"
        >
            <a-spin :spinning="spinning" tip="上传中...">
            <a-form-model
                ref="addDatasetForm"
                :model="add_dataset_form"
                :rules="add_dataset_rules"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 14 }"
            >
                <a-form-model-item label="数据集文件" prop="file">
                    <a-upload
                        :file-list="add_dataset_form.file"
                        :before-upload="beforeUpload"
                        :remove="handleRemove"
                    >
                        <a-button> <a-icon type="upload" /> 选择文件 </a-button>
                    </a-upload>
                </a-form-model-item>
                <a-form-model-item label="命名" prop="name">
                    <a-input v-model="add_dataset_form.name" />
                </a-form-model-item>
                <a-form-model-item label="描述" prop="description">
                    <a-textarea placeholder="选填" :rows="4" v-model="add_dataset_form.description" />
                </a-form-model-item>
                <a-form-model-item label="分割符" prop="separator" :wrapper-col="{ span: 6}">
                    <a-input v-model="add_dataset_form.separator" />
                </a-form-model-item>

                <a-form-model-item
                    v-for="(column, index) in add_dataset_form.columns"
                    :key="column.key"
                    v-bind="index === 0 ? {} : formItemLayoutWithOutLabel"
                    :label="index === 0 ? '列名' : ''"
                    :prop="'columns.' + index + '.col_name'"
                    :rules="{
                        required: true,
                        message: '列名不得为空',
                        trigger: 'blur',
                    }"
                >
                    <a-input
                        v-model="column.col_name"
                        style="width: 40%; margin-right: 8px"
                    />
                    <a-select
                        v-model="column.data_type"
                        placeholder="数据类型"
                        style="width: 40%; margin-right: 8px"
                    >
                        <a-select-option value=0>
                            String
                        </a-select-option>
                        <a-select-option value=1>
                            Integer
                        </a-select-option>
                        <a-select-option value=2>
                            Float
                        </a-select-option>
                    </a-select>
                    <a-icon
                        v-if="add_dataset_form.columns.length > 1"
                        class="dynamic-delete-button"
                        type="minus-circle-o"
                        :disabled="add_dataset_form.columns.length === 1"
                        @click="removeColumn(column)"
                    />
                </a-form-model-item>
                <a-form-model-item :wrapper-col="{ span: 14, offset: 5 }">
                    <a-button type="dashed" style="width: 60%" @click="addColumn">
                        <a-icon type="plus" /> 添加一列
                    </a-button>
                </a-form-model-item>

                <a-form-model-item :wrapper-col="{ span: 14, offset: 5 }">
                    <a-button type="primary" @click="submitAddDataset">提交</a-button>
                </a-form-model-item>
            </a-form-model>
            </a-spin>
        </a-modal>
        <a-table
            :columns="columns"
            :data-source="data"
            :pagination="pagination"
            :row-selection="rowSelection"
            :loading="table_loading"
            @change="handleTableChange"
        >
            <a @click="() => enterDataset(record.key)"
                slot="name"
                slot-scope="text, record"
            >{{ text }}</a>
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
        <a-modal
            title="数据集变更"
            :visible="modify_dataset_modal"
            :footer="null"
            @cancel="closeModifyDatasetModal"
        >
            <a-form
                :form="modify_dataset_form"
                :label-col="{ span: 5 }"
                :wrapper-col="{ span: 12 }"
                @submit="submitModification"
            >
                <a-form-item label="数据集名称">
                    <a-input :value="tmp_name" />
                </a-form-item>
                <a-form-item label="数据集描述">
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
        title: '数据集名称',
        dataIndex: 'name',
        scopedSlots: { customRender: 'name' },
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
    name: "Dataset",
    data() {
        return {
            project_name: "",
            columns: columns,
            data: [],
            selected_row_keys: {},
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
            add_dataset_modal: false,
            add_dataset_form: {
                file: [],
                name: '',
                description: '',
                separator: '',
                columns: [],
            },
            add_dataset_rules: {
                file: [{ required: true, message: '请选择数据集文件！', trigger: 'change' }],
                name: [{ required: true, message: '命名不得为空！', trigger: 'blur' }],
                separator: [
                    { required: true, message: '分割符不得为空！', trigger: 'blur' },
                    { max: 1, message: '分割符最多为一个字符！', trigger: 'blur' },
                ],
            },
            formItemLayoutWithOutLabel: { wrapperCol: { span: 14, offset: 5 } },
            spinning: false,
            table_loading: false,
            modify_dataset_modal: false,
            modify_dataset_form: this.$form.createForm(this, { name: 'modify_dataset' }),
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

        // 获取所有数据集
        this.$axios({
            method: 'post',
            url: '/dataset/get-all/',
            data: {
              "project_id": Number(this.$route.params.project_id),
              "num": 5,
              "start": 1
            }
        }).then((response) => {
            console.log(response.data);
            this.data = response.data.datasets;
            this.pagination.total = response.data.total;
            this.table_loading = false;
        })
    },
    methods: {
        // 点击添加数据集
        addDataset() {
            this.add_dataset_modal = true;
        },

        // 关闭添加数据集对话框
        closeAddDatasetModal() {
            this.add_dataset_modal = false;
        },

        // 移除上传的数据集
        handleRemove() {
            this.add_dataset_form.file = [];
        },

        // 上传文件之前的钩子
        beforeUpload(file) {
            this.add_dataset_form.file = [file];
            return false;
        },

        // 添加一列
        addColumn() {
            this.add_dataset_form.columns.push({
                col_name: '',
                data_type: undefined,
                key: Date.now(),
            });
        },

        // 删除一列
        removeColumn(item) {
            let index = this.add_dataset_form.columns.indexOf(item);
            if (index !== -1) {
                this.add_dataset_form.columns.splice(index, 1);
            }
        },

        // 提交添加数据集
        submitAddDataset() {
            
            this.$refs.addDatasetForm.validate(valid => {
                if (valid) {
                    console.log('Received values of form: ');
                    console.log(this.add_dataset_form);
                    
                    this.spinning = true;
                    
                    const formData = new FormData();
                    formData.append("username", this.$cookies.get("username"));
                    formData.append("project_id", Number(this.$route.params.project_id));
                    formData.append("name", this.add_dataset_form.name);
                    formData.append("description", this.add_dataset_form.description);
                    formData.append("separator", this.add_dataset_form.separator);
                    formData.append("columns", JSON.stringify(this.add_dataset_form.columns));
                    formData.append("file", this.add_dataset_form.file[0])
                    this.$axios({
                        method: 'post',
                        url: '/dataset/upload/',
                        data: formData
                    }).then((response) => {
                        console.log(response.data);
                        this.spinning = false;
                        if (response.data.status == 0) {
                            this.$message.error('添加数据集失败！');
                        } else if (response.data.status == 1) {
                            this.$message.success('添加成功！');
                            this.$router.go(0);
                        } else {
                            this.$message.error('非法状态！');
                        }
                    })
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
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

        // 打开数据集
        enterDataset(key) {
            console.log("数据集的 key 是:");
            console.log(key);
            this.$router.push("/dashboard/workspace/project/" + this.$route.params.project_id + "/dataset/" + String(this.data[Number(key) - 1].id))
        },

        // 点击修改数据集
        modifyDataset(key) {
            console.log("修改数据集");
            console.log(this.data[Number(key) - 1].name);
            console.log(this.data[Number(key) - 1].description);
            this.tmp_name = this.data[Number(key) - 1].name;
            this.tmp_description = this.data[Number(key) - 1].description;
            this.modify_dataset_modal = true;
        },

        // 删除一个数据集
        deleteOne(key) {
            console.log("要删除的数据集是:");
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

        // 关闭修改数据集对话框
        closeModifyDatasetModal() {
            this.modify_dataset_modal = false;
        },

        // 提交项目变更
        submitModification(e) {
            e.preventDefault();
            this.modify_dataset_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                    // TODO
                }
            })
        },
    }
}
</script>
