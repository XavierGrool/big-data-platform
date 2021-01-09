<template>
<a-layout style="padding: 0 24px 24px">
    <a-spin :spinning="spinning" tip="加载中...">
    <a-breadcrumb style="margin: 16px 0">
        <a-breadcrumb-item>Workspace</a-breadcrumb-item>
        <a-breadcrumb-item>Projects</a-breadcrumb-item>
        <a-breadcrumb-item>{{ project_name }}</a-breadcrumb-item>
        <a-breadcrumb-item>Prediction</a-breadcrumb-item>
    </a-breadcrumb>
    <a-layout-content
        :style="{ background: '#fff', padding: '24px', margin: 0, minHeight: '280px' }"
    >
        <a-layout>
            <a-layout v-if="dataset_num == 0" style="background: #fff">
                <a-result
                    status="404"
                    title="该项目还没有数据集"
                    sub-title="—— 先去导入数据吧！"
                >
                    <template #extra>
                    <a-button type="primary">
                        返回
                    </a-button>
                    </template>
                </a-result>
            </a-layout>
            <a-layout v-else-if="model_num == 0" style="background: #fff">
                <a-result
                    status="404"
                    title="该项目还没有模型"
                    sub-title="—— 先去添加模型吧！"
                >
                    <template #extra>
                    <a-button type="primary">
                        返回
                    </a-button>
                    </template>
                </a-result>
            </a-layout>
            <a-layout v-else style="background: #fff">
                <a-layout-content style="padding-right: 160px">
                    <div>
                        <div style="font-size: 24px; margin-bottom: 16px">选择模型</div>
                        <a-select
                            placeholder="选择模型"
                            style="width: 240px"
                            @change="handleModelSelectedChanged"
                        >
                            <a-select-option
                                v-for="model in models"
                                :key="model.id"
                                :value="model.id"
                            >
                                {{ model.name }}
                            </a-select-option>
                        </a-select>
                    </div>
                    <div v-if="progress > 1">
                        <a-divider />
                        <div style="font-size: 24px; margin-bottom: 16px">选择数据集</div>
                        <a-select
                            placeholder="选择数据集"
                            style="width: 240px"
                            @change="handleDatasetSelectedChanged"
                        >
                            <a-select-option
                                v-for="dataset in datasets"
                                :key="dataset.id"
                                :value="dataset.id"
                            >
                                {{ dataset.name }}
                            </a-select-option>
                        </a-select>
                    </div>
                    <div v-if="progress > 2">
                        <a-divider />
                        <div style="font-size: 24px; margin-bottom: 24px">选择 Features</div>
                        <a-space direction="vertical" size="middle">
                            <a-checkbox-group
                                v-model="checkedFeatures"
                                :options="featureOptions"
                            />
                            <a-button
                                type="primary" 
                                @click="biginToPredict"
                            >
                                开始预测<a-icon type="check-circle" />
                            </a-button>
                        </a-space>
                    </div>
                    <div v-if="progress > 4">
                        <a-divider />
                        <div style="font-size: 24px; margin-bottom: 24px">预测结果</div>
                        <a-table
                            :pagination="false"
                            :columns="table_columns"
                            :data-source="table_data"
                        >
                        </a-table>
                    </div>
                </a-layout-content>
                <a-layout-sider style="background: #fff; margin-right: 120px">
                    <a-affix :offset-top="160">
                    <a-steps
                        direction="vertical"
                        size="small"
                        :current="progress - 1"
                    >
                        <a-step
                            v-for="step in steps"
                            :key="step.id"
                            :title="step.content"
                        />
                    </a-steps>
                    </a-affix>
                </a-layout-sider>
            </a-layout>
        </a-layout>
    </a-layout-content>
    </a-spin>
</a-layout>
</template>

<script>
export default {
    name: "Prediction",
    data() {
        return {
            project_name: "",
            spinning: false,
            dataset_num: 0,
            datasets: [],
            model_num: 0,
            models: [],
            progress: 1,
            steps: [
                {id: 0, content: "选择模型"},
                {id: 1, content: "选择数据集"},
                {id: 2, content: "选择 Features"},
                {id: 3, content: "预测分析"},
                {id: 4, content: "结果展示"},
            ],
            selected_model_id: 0,
            selected_dataset_id: 0,
            checkedFeatures: [],
            featureOptions: [],
            table_columns: [],
            table_data: []
        }
    },

    created() {
        console.log(this.$route.params.project_id)
        this.spinning = true;

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

        // 获取当前项目下的数据集
        this.$axios({
            method: 'post',
            url: '/prediction/get-dataset/',
            data: {
                "id": Number(this.$route.params.project_id)
            }
        }).then((response) => {
            console.log(response.data);
            this.dataset_num = response.data.dataset_num;
            this.datasets = response.data.datasets;
        });

        // 获取当前项目下的模型
        this.$axios({
            method: 'post',
            url: '/prediction/get-model/',
            data: {
                "id": Number(this.$route.params.project_id)
            }
        }).then((response) => {
            console.log(response.data);
            this.model_num = response.data.model_num;
            this.models = response.data.models;
            this.spinning = false;
        });
    },
    methods: {
        // 选择的模型发生变化
        handleModelSelectedChanged(value) {
            console.log("选择的模型发生变化")
            console.log(`selected ${value}`);
            this.selected_dataset_id = 0;
            this.selected_model_id = value;
            this.progress = 2;
        },

        // 选择的数据集发生变化
        handleDatasetSelectedChanged(value) {
            console.log("选择的数据集发生变化")
            console.log(`selected ${value}`);
            this.featureOptions = [];
            this.checkedFeatures = [];
            this.selected_dataset_id = value;
            this.progress = 2;
            this.spinning = true;
            this.$axios({
                method: 'post',
                url: '/prediction/get-columns/',
                data: {
                    "dataset_id": value
                }
            }).then((response) => {
                console.log(response.data);
                for (var i = 0; i < response.data.columns.length; i++) {
                    var tmp = new Object();
                    tmp.label = response.data.columns[i].name;
                    tmp.value = response.data.columns[i].index;
                    this.featureOptions.push(tmp);
                }
                this.progress = 3;
                this.spinning = false;
            });
        },

        // 开始预测
        biginToPredict() {
            console.log(this.checkedFeatures)
            if (this.checkedFeatures.length == 0) {
                this.$message.error('请选择 features');
            } else {
                this.progress = 4;
                this.spinning = true;
                this.$axios({
                    method: 'post',
                    url: '/prediction/predict/',
                    data: {
                        "model_id": this.selected_model_id,
                        "dataset_id": this.selected_dataset_id,
                        "features": this.checkedFeatures,
                    }
                }).then((response) => {
                    console.log(response.data);
                    this.table_data = response.data.predictions;
                    this.table_columns = response.data.columns;
                    this.spinning = false;
                    this.progress = 5;
                });
            }
        },
    }
}
</script>
