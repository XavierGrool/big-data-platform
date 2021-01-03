<template>
<a-layout>
    <a-layout-sider width="200" style="background: #fff">
    <div style="height:64px;padding-top:20px;">
        <a @click="returnToModels" style="fontSize:24px;margin-left:88px">
            <a-icon type="left" />
        </a>
    </div>
    </a-layout-sider>
    <a-layout style="padding: 0 24px 24px">
        <a-spin :spinning="spinning" tip="加载中...">
        <a-breadcrumb style="margin: 16px 0">
            <a-breadcrumb-item>Workspace</a-breadcrumb-item>
            <a-breadcrumb-item>Projects</a-breadcrumb-item>
            <a-breadcrumb-item>{{ project_name }}</a-breadcrumb-item>
            <a-breadcrumb-item>Model</a-breadcrumb-item>
            <a-breadcrumb-item>Add</a-breadcrumb-item>
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
                <a-layout v-else style="background: #fff">
                    <a-layout-content style="padding-right: 160px">
                        <div>
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
                        <div v-if="progress > 1">
                            <a-divider />
                            <div style="font-size: 24px; margin-bottom: 16px">选择 Label</div>
                            <a-radio-group
                                v-model="checkedLabel"
                                @change="onLabelSelectedChange"
                            >
                                <a-radio
                                    v-for="column in columns"
                                    :key="column.index"
                                    :value="column.index"
                                >
                                    {{ column.name }}
                                </a-radio>
                            </a-radio-group>
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
                                    @click="onFeatureSelectedConfirmed"
                                >
                                    选定<a-icon type="check-circle" />
                                </a-button>
                            </a-space>
                        </div>
                        <div v-if="progress > 3">
                            <a-divider />
                            <div style="font-size: 24px; margin-bottom: 16px">确定问题分类</div>
                            <div style="font-size: 16px; margin-bottom: 7px">您的问题属于：</div>
                            <a-radio-group
                                v-model="checkedProblemType"
                                @change="onProblemTypeChange"
                            >
                                <a-radio :value=1>二分类问题</a-radio>
                                <a-radio :value=2>多分类问题</a-radio>
                            </a-radio-group>
                        </div>
                        <div v-if="progress > 4">
                            <a-divider />
                            <div style="font-size: 24px; margin-bottom: 48px">配置模型</div>
                            <div style="margin-bottom: 4px">以下是我们为您推荐的算法模型，其中的参数也进行了自动设置。<br/></div>
                            <div style="margin-bottom: 48px">当然，您也可以自行调整。</div>
                            <div style="font-size: 16px; margin-bottom: 7px">算法模型：</div>
                            <a-select
                                placeholder="请选择一种算法"
                                style="width: 250px; margin-bottom: 36px"
                                v-model="selected_classifier_id"
                                @change="handleClassifierSelectedChanged"
                            >
                                <a-select-option
                                    v-for="classifier in classifiers"
                                    :key="classifier.id"
                                >
                                    {{ classifier.name }}
                                </a-select-option>
                            </a-select>
                            <div style="width: 60%"><a-divider orientation="left">参数设置</a-divider></div>
                            <a-form-model
                                ref="modelConfigForm"
                                layout="horizontal"
                                style="width: 40%"
                                :model="model_config_form"
                                :rules="model_config_rules"
                            >
                                <a-form-model-item
                                    label="aggregationDepth"
                                    prop="lr_aggregation_depth"
                                    v-if="selected_classifier_id == 1"
                                >
                                    <a-input v-model="model_config_form.lr_aggregation_depth" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="elasticNetParam"
                                    prop="lr_elastic_net_param"
                                    v-if="selected_classifier_id == 1"
                                >
                                    <a-input v-model="model_config_form.lr_elastic_net_param" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="fitIntercept"
                                    prop="lr_fit_intercept"
                                    v-if="selected_classifier_id == 1"
                                >
                                    <a-select
                                        v-model="model_config_form.lr_fit_intercept"
                                        style="width: 100px"
                                    >
                                        <a-select-option value="true">True</a-select-option>
                                        <a-select-option value="false">False</a-select-option>
                                    </a-select>
                                </a-form-model-item>
                                <a-form-model-item
                                    label="maxIter"
                                    prop="lr_max_iter"
                                    v-if="selected_classifier_id == 1"
                                >
                                    <a-input v-model="model_config_form.lr_max_iter" />
                                    </a-form-model-item>
                                <a-form-model-item
                                    label="regParam"
                                    prop="lr_reg_param"
                                    v-if="selected_classifier_id == 1"
                                >
                                    <a-input v-model="model_config_form.lr_reg_param" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="maxDepth"
                                    prop="dt_max_depth"
                                    v-if="selected_classifier_id == 2"
                                >
                                    <a-input v-model="model_config_form.dt_max_depth" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="impurity"
                                    prop="dt_impurity"
                                    v-if="selected_classifier_id == 2"
                                >
                                    <a-select
                                        v-model="model_config_form.dt_impurity"
                                        style="width: 120px"
                                    >
                                        <a-select-option value="entropy">entropy</a-select-option>
                                        <a-select-option value="gini">gini</a-select-option>
                                    </a-select>
                                </a-form-model-item>
                                <a-form-model-item
                                    label="impurity"
                                    prop="rf_impurity"
                                    v-if="selected_classifier_id == 3"
                                >
                                    <a-select
                                        v-model="model_config_form.rf_impurity"
                                        style="width: 120px"
                                    >
                                        <a-select-option value="entropy">entropy</a-select-option>
                                        <a-select-option value="gini">gini</a-select-option>
                                    </a-select>
                                </a-form-model-item>
                                <a-form-model-item
                                    label="maxDepth"
                                    prop="rf_max_depth"
                                    v-if="selected_classifier_id == 3"
                                >
                                    <a-input v-model="model_config_form.rf_max_depth" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="numtrees"
                                    prop="rf_num_trees"
                                    v-if="selected_classifier_id == 3"
                                >
                                    <a-input v-model="model_config_form.rf_num_trees" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="maxDepth"
                                    prop="gbt_max_depth"
                                    v-if="selected_classifier_id == 4"
                                >
                                    <a-input v-model="model_config_form.gbt_max_depth" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="maxIter"
                                    prop="gbt_max_iter"
                                    v-if="selected_classifier_id == 4"
                                >
                                    <a-input v-model="model_config_form.gbt_max_iter" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="stepSize"
                                    prop="gbt_step_size"
                                    v-if="selected_classifier_id == 4"
                                >
                                    <a-input v-model="model_config_form.gbt_step_size" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="subsamplingRate"
                                    prop="gbt_subsampling_rate"
                                    v-if="selected_classifier_id == 4"
                                >
                                    <a-input v-model="model_config_form.gbt_subsampling_rate" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="smoothing"
                                    prop="nb_smoothing"
                                    v-if="selected_classifier_id == 5"
                                >
                                    <a-input v-model="model_config_form.nb_smoothing" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="modelType"
                                    prop="nb_model_type"
                                    v-if="selected_classifier_id == 5"
                                >
                                    <a-select
                                        v-model="model_config_form.nb_model_type"
                                        style="width: 140px"
                                    >
                                        <a-select-option value="multinomial">multinomial</a-select-option>
                                        <a-select-option value="bernoulli">bernoulli</a-select-option>
                                        <a-select-option value="gaussian">gaussian</a-select-option>
                                    </a-select>
                                </a-form-model-item>
                                <a-form-model-item
                                    label="maxIter"
                                    prop="lsvc_max_iter"
                                    v-if="selected_classifier_id == 6"
                                >
                                    <a-input v-model="model_config_form.lsvc_max_iter" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="regParam"
                                    prop="lsvc_reg_param"
                                    v-if="selected_classifier_id == 6"
                                >
                                    <a-input v-model="model_config_form.lsvc_reg_param" />
                                </a-form-model-item>
                                <a-form-model-item
                                    label="fitIntercept"
                                    prop="lsvc_fit_intercept"
                                    v-if="selected_classifier_id == 6"
                                >
                                    <a-select
                                        v-model="model_config_form.lsvc_fit_intercept"
                                        style="width: 100px"
                                    >
                                        <a-select-option value="true">True</a-select-option>
                                        <a-select-option value="false">False</a-select-option>
                                    </a-select>
                                </a-form-model-item>
                                <a-form-model-item
                                    label="standardization"
                                    prop="lsvc_standardization"
                                    v-if="selected_classifier_id == 6"
                                >
                                    <a-select
                                        v-model="model_config_form.lsvc_standardization"
                                        style="width: 100px"
                                    >
                                        <a-select-option value="true">True</a-select-option>
                                        <a-select-option value="false">False</a-select-option>
                                    </a-select>
                                </a-form-model-item>
                                <a-form-model-item
                                    label="aggregationDepth"
                                    prop="lsvc_aggregation_depth"
                                    v-if="selected_classifier_id == 6"
                                >
                                    <a-input v-model="model_config_form.lsvc_aggregation_depth" />
                                </a-form-model-item>
                                <a-form-model-item v-if="selected_classifier_id > 0">
                                    <a-button type="primary" @click="trainAModel">
                                        开始训练
                                    </a-button>
                                </a-form-model-item>
                            </a-form-model>
                        </div>
                        <div v-if="progress > 6">
                            <a-card
                                style="width:50%"
                                title="训练结果"
                                v-if="checkedProblemType == 1"
                                :tab-list="tabList[0]"
                                :active-tab-key="key"
                                @tabChange="key => onTabChange(key, 'key')"
                            >
                                <div v-if="key == 'tab1'">
                                    <a-space size="large">
                                    <a-statistic
                                        title="训练集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.train_roc * 100"
                                    />
                                    <a-statistic
                                        title="测试集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.test_roc * 100" 
                                    />
                                    </a-space>
                                </div>
                                <div v-if="key == 'tab2'">
                                    <a-space size="large">
                                    <a-statistic
                                        title="训练集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.train_pr * 100"
                                    />
                                    <a-statistic
                                        title="测试集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.test_pr * 100" 
                                    />
                                    </a-space>
                                </div>
                            </a-card>
                            <a-card
                                style="width:50%"
                                title="训练结果"
                                v-if="checkedProblemType == 2"
                                :tab-list="tabList[1]"
                                :active-tab-key="key"
                                @tabChange="key => onTabChange(key, 'key')"
                            >
                                <div v-if="key === 'tab1'">
                                    <a-space size="large">
                                    <a-statistic
                                        title="训练集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.train_acc * 100"
                                    />
                                    <a-statistic
                                        title="测试集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.test_acc * 100" 
                                    />
                                    </a-space>
                                </div>
                                <div v-if="key === 'tab2'">
                                    <a-space size="large">
                                    <a-statistic
                                        title="训练集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.train_f1 * 100"
                                    />
                                    <a-statistic
                                        title="测试集"
                                        suffix="%"
                                        :precision="5"
                                        :value="train_results.test_f1 * 100" 
                                    />
                                    </a-space>
                                </div>
                            </a-card>
                            <a-divider />
                            <div style="font-size: 24px; margin-bottom: 24px">保存模型</div>
                            <div style="margin-bottom: 4px">您希望保存该模型吗？<br/></div>
                            <div style="margin-bottom: 36px">您也可以重新调整模型和参数，再次进行训练。</div>
                            <a-form
                                style="width: 60%"
                                :form="save_model_form"
                                @submit="submitSaveModel"
                            >
                                <a-form-item label="模型命名">
                                    <a-input
                                        v-decorator="['name', { rules: [{ required: true, message: '模型名字不得为空!' }] }]"
                                    />
                                </a-form-item>
                                <a-form-item label="模型描述">
                                    <a-textarea placeholder="选填" v-decorator="['description']" :rows="4" />
                                </a-form-item>
                                <a-form-item>
                                    <a-button type="primary" html-type="submit">
                                        保存模型
                                    </a-button>
                                </a-form-item>
                            </a-form>
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
</a-layout>
</template>

<script>
const binary_class_classifiers = [
    {
        id: 1,
        name: 'Logistic Regression',
    },
    {
        id: 2,
        name: 'Decision Tree Classifier',
    },
    {
        id: 3,
        name: 'Random Forest Classifier',
    },
    {
        id: 4,
        name: 'Gradient-boosted Tree Classifier',
    },
    {
        id: 5,
        name: 'Naive Bayes',
    },
    {
        id: 6,
        name: 'Linear Support Vector Machine',
    },
];

const multi_class_classifiers = [
    {
        id: 2,
        name: 'Decision Tree Classifier',
    },
    {
        id: 3,
        name: 'Random Forest Classifier',
    },
    {
        id: 5,
        name: 'Naive Bayes',
    },
];

export default {
    name: "AddModel",
    data() {
        let checkLRAggregationDepth = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('aggregationDepth 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('aggregationDepth 必须为整形！'));
            } else {
                if (Number(value) < 2) {
                    callback(new Error('aggregationDepth 的值必须大于等于 2'));
                } else {
                    callback();
                }
            }
        };
        let checkLRElasticNetParam = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('elasticNetParam 不得为空!'));
            }
            if (Number.isNaN(Number(value))) {
                callback(new Error('elasticNetParam 不得为字符串！'));
            } else {
                if (Number(value) < 0 || Number(value) > 1) {
                    callback(new Error('elasticNetParam 的取值范围为 [0, 1]'));
                } else {
                    callback();
                }
            }
        };
        let checkLRMaxIter = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('maxIter 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('maxIter 必须为整形！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('maxIter 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkLRRegParam = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('regParam 不得为空!'));
            }
            if (Number.isNaN(Number(value))) {
                callback(new Error('regParam 不得为字符串！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('regParam 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkDTMaxDepth = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('maxDepth 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('maxDepth 必须为整形！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('maxDepth 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkRFMaxDepth = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('maxDepth 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('maxDepth 必须为整形！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('maxDepth 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkRFNumTrees = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('numtrees 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('numtrees 必须为整形！'));
            } else {
                if (Number(value) < 1) {
                    callback(new Error('numtrees 的值必须大于等于 1'));
                } else {
                    callback();
                }
            }
        };
        let checkGBTMaxDepth = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('maxDepth 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('maxDepth 必须为整形！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('maxDepth 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkGBTMaxIter = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('maxIter 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('maxIter 必须为整形！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('maxIter 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkGBTStepSize = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('stepSize 不得为空!'));
            }
            if (Number.isNaN(Number(value))) {
                callback(new Error('stepSize 不得为字符串！'));
            } else {
                if (Number(value) <= 0 || Number(value) > 1) {
                    callback(new Error('stepSize 的取值范围为 (0, 1]'));
                } else {
                    callback();
                }
            }
        };
        let checkGBTSubsamplingRate = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('subsamplingRate 不得为空!'));
            }
            if (Number.isNaN(Number(value))) {
                callback(new Error('subsamplingRate 不得为字符串！'));
            } else {
                if (Number(value) <= 0 || Number(value) > 1) {
                    callback(new Error('subsamplingRate 的取值范围为 (0, 1]'));
                } else {
                    callback();
                }
            }
        };
        let checkNBSmoothing = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('smoothing 不得为空!'));
            }
            if (Number.isNaN(Number(value))) {
                callback(new Error('smoothing 不得为字符串！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('smoothing 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkLSVCMaxIter = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('maxIter 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('maxIter 必须为整形！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('maxIter 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkLSVCRegParam = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('regParam 不得为空!'));
            }
            if (Number.isNaN(Number(value))) {
                callback(new Error('regParam 不得为字符串！'));
            } else {
                if (Number(value) < 0) {
                    callback(new Error('regParam 的值必须大于等于 0'));
                } else {
                    callback();
                }
            }
        };
        let checkLSVCAggregationDepth = (rule, value, callback) => {
            if (!value) {
                return callback(new Error('aggregationDepth 不得为空!'));
            }
            if (!Number.isInteger(Number(value))) {
                callback(new Error('aggregationDepth 必须为整形！'));
            } else {
                if (Number(value) < 2) {
                    callback(new Error('aggregationDepth 的值必须大于等于 2'));
                } else {
                    callback();
                }
            }
        };
        return {
            spinning: false,
            progress: 1,
            project_name: "",
            select_dataset_form: this.$form.createForm(this, { name: 'select_dataset' }),
            select_label_form: this.$form.createForm(this, { name: 'select_label' }),
            select_features_form: this.$form.createForm(this, { name: 'select_features' }),
            select_problem_type_form: this.$form.createForm(this, { name: 'select_problem_type' }),
            save_model_form: this.$form.createForm(this, { name: 'save_model' }),
            dataset_num: 0,
            datasets: [],
            selected_dataset_id: 0,
            steps: [
                {id: 0, content: "选择数据集"},
                {id: 1, content: "选择 Label"},
                {id: 2, content: "选择 Features"},
                {id: 3, content: "确定问题分类"},
                {id: 4, content: "配置模型"},
                {id: 5, content: "模型训练"},
                {id: 6, content: "保存模型"},
            ],
            columns: [],
            checkedLabel: "",
            checkedFeatures: [],
            featureOptions: [],
            checkedProblemType: 0,
            classifiers: [],
            selected_classifier_id: 0,
            model_config_form: {
                lr_aggregation_depth: "2",
                lr_elastic_net_param: "0.0",
                lr_fit_intercept: "true",
                lr_max_iter: "100",
                lr_reg_param: "0.0",
                dt_max_depth: "5",
                dt_impurity: "gini",
                rf_impurity: "gini",
                rf_max_depth: "5",
                rf_num_trees: "20",
                gbt_max_depth: "5",
                gbt_max_iter: "20",
                gbt_step_size: "0.1",
                gbt_subsampling_rate: "1.0",
                lsvc_max_iter: "100",
                lsvc_reg_param: "0.0",
                lsvc_fit_intercept: "true",
                lsvc_standardization: "true",
                lsvc_aggregation_depth: "2",
                nb_smoothing: "1.0",
                nb_model_type: "multinomial",
            },
            model_config_rules: {
                lr_aggregation_depth: [{ validator: checkLRAggregationDepth, trigger: 'blur' }],
                lr_elastic_net_param: [{ validator: checkLRElasticNetParam, trigger: 'blur' }],
                lr_max_iter: [{ validator: checkLRMaxIter, trigger: 'blur' }],
                lr_reg_param: [{ validator: checkLRRegParam, trigger: 'blur' }],
                dt_max_depth: [{ validator: checkDTMaxDepth, trigger: 'blur' }],
                rf_max_depth: [{ validator: checkRFMaxDepth, trigger: 'blur' }],
                rf_num_trees: [{ validator: checkRFNumTrees, trigger: 'blur' }],
                gbt_max_depth: [{ validator: checkGBTMaxDepth, trigger: 'blur' }],
                gbt_max_iter: [{ validator: checkGBTMaxIter, trigger: 'blur' }],
                gbt_step_size: [{ validator: checkGBTStepSize, trigger: 'blur' }],
                gbt_subsampling_rate: [{ validator: checkGBTSubsamplingRate, trigger: 'blur' }],
                nb_smoothing: [{ validator: checkNBSmoothing, trigger: 'blur' }],
                lsvc_max_iter: [{ validator: checkLSVCMaxIter, trigger: 'blur' }],
                lsvc_reg_param: [{ validator: checkLSVCRegParam, trigger: 'blur' }],
                lsvc_aggregation_depth: [{ validator: checkLSVCAggregationDepth, trigger: 'blur' }],
            },
            train_results: {
                train_roc: 0,
                test_roc: 0,
                train_pr: 0,
                test_pr: 0,
                train_acc: 0,
                test_acc: 0,
                train_f1: 0,
                test_f1: 0
            },
            tabList: [
                [{key: "tab1", tab: 'ROC'}, {key: "tab2", tab: 'PR'}],
                [{key: "tab1", tab: 'ACC'}, {key: "tab2", tab: 'F1'}]
            ],
            key: "tab1",
        }
    },
    created() {
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
        });

        // 获取当前项目下的数据集
        this.$axios({
            method: 'post',
            url: '/add-model/get-dataset/',
            data: {
                "id": Number(this.$route.params.project_id)
            }
        }).then((response) => {
            console.log(response.data);
            this.dataset_num = response.data.dataset_num;
            this.datasets = response.data.datasets;
            this.spinning = false;
        });
    },
    methods: {
        // 返回模型管理
        returnToModels() {
            var path = this.$route.path;
            this.$router.push(path.slice(0, path.lastIndexOf("/")))
        },

        // 选择的数据集发生变化
        handleDatasetSelectedChanged(value) {
            console.log("选择的数据集发生变化")
            console.log(`selected ${value}`);
            this.checkedLabel = "";
            this.selected_dataset_id = value;
            this.progress = 1;
            this.spinning = true;
            this.$axios({
                method: 'post',
                url: '/add-model/get-columns/',
                data: {
                    "dataset_id": value
                }
            }).then((response) => {
                console.log(response.data);
                this.columns = response.data.columns;
                this.progress = 2;
                this.spinning = false;
            });
        },

        // 当选择的 label 发生变化
        onLabelSelectedChange(e) {
            console.log("当前选中的 label 是:");
            console.log(this.checkedLabel);
            this.progress = 2;
            this.featureOptions = [];
            this.checkedFeatures = [];
            for (var i = 0; i < this.columns.length; i++) {
                if (e.target.value != this.columns[i].index) {
                    var tmp = new Object();
                    tmp.label = this.columns[i].name;
                    tmp.value = this.columns[i].index;
                    this.featureOptions.push(tmp);
                }
            }
            this.progress = 3;
        },

        // 当确认选定的 features 时
        onFeatureSelectedConfirmed() {
            console.log(this.checkedFeatures)
            this.checkedProblemType = 0;
            if (this.checkedFeatures.length == 0) {
                this.$message.error('请选择 features');
            } else {
                this.progress = 4;
            }
        },

        // 当问题类型发生变更时
        onProblemTypeChange() {
            console.log("当前选择的问题分类是:");
            console.log(this.checkedProblemType);
            if (this.checkedProblemType == 1) {
                this.classifiers = binary_class_classifiers;
                this.selected_classifier_id = 4;
            } else if (this.checkedProblemType == 2) {
                this.classifiers = multi_class_classifiers;
                this.selected_classifier_id = 3;
            }
            this.progress = 5;
        },

        // 当选择的分类算法发生变化时
        handleClassifierSelectedChanged(value) {
            console.log("选择的分类算法发生变化")
            console.log(`selected ${value}`);

            // 重置各默认参数
            this.model_config_form.lr_aggregation_depth = "2";
            this.model_config_form.lr_elastic_net_param = "0.0";
            this.model_config_form.lr_fit_intercept = "true";
            this.model_config_form.lr_max_iter = "100";
            this.model_config_form.lr_reg_param = "0.0";
            this.model_config_form.dt_max_depth = "5";
            this.model_config_form.dt_impurity = "gini";
            this.model_config_form.rf_impurity = "gini";
            this.model_config_form.rf_max_depth = "5";
            this.model_config_form.rf_num_trees = "20";
            this.model_config_form.gbt_max_depth = "5";
            this.model_config_form.gbt_max_iter = "20";
            this.model_config_form.gbt_step_size = "0.1";
            this.model_config_form.gbt_subsampling_rate = "1.0";
            this.model_config_form.lsvc_max_iter = "100";
            this.model_config_form.lsvc_reg_param = "0.0";
            this.model_config_form.lsvc_fit_intercept = "true";
            this.model_config_form.lsvc_standardization = "true";
            this.model_config_form.lsvc_aggregation_depth = "2";
            this.model_config_form.nb_smoothing = "1.0";
            this.model_config_form.nb_model_type = "multinomial";

            this.selected_classifier_id = value;
        },

        // 训练模型
        trainAModel() {
            console.log("开始训练！");
            this.progress = 6;
            this.spinning = true;
            this.$axios({
                method: 'post',
                url: '/add-model/train/',
                data: {
                    "dataset_id": this.selected_dataset_id,
                    "label": this.checkedLabel,
                    "features": this.checkedFeatures,
                    "problem_type": this.checkedProblemType,
                    "classifier": this.selected_classifier_id,
                    "classifier_params": this.model_config_form
                }
            }).then((response) => {
                console.log(response.data);
                if (this.checkedProblemType == 1) { // 二分类问题
                    this.train_results.train_roc = response.data.results.train_roc;
                    this.train_results.test_roc = response.data.results.test_roc;
                    this.train_results.train_pr = response.data.results.train_pr;
                    this.train_results.test_pr = response.data.results.test_pr;
                } else if (this.checkedProblemType == 2) { // 多分类问题
                    this.train_results.train_acc = response.data.results.train_acc;
                    this.train_results.test_acc = response.data.results.test_acc;
                    this.train_results.train_f1 = response.data.results.train_f1;
                    this.train_results.test_f1 = response.data.results.test_f1;
                }
                this.spinning = false;
                this.progress = 7;
            });
        },

        // 保存模型
        submitSaveModel(e) {
            e.preventDefault();
            this.save_model_form.validateFields((err, values) => {
                if (!err) {
                    console.log('Received values of form: ', values);
                    this.spinning = true;
                    this.$axios({
                        method: 'post',
                        url: '/add-model/save/',
                        data: {
                            "dataset_id": this.selected_dataset_id,
                            "label": this.checkedLabel,
                            "features": this.checkedFeatures,
                            "problem_type": this.checkedProblemType,
                            "classifier": this.selected_classifier_id,
                            "classifier_params": this.model_config_form,
                            "model_name": values.name,
                            "model_description": values.description == undefined? "" : values.description
                        }
                    }).then((response) => {
                        console.log(response.data);
                        this.spinning = false;
                        if (response.data.status == 0) {
                            this.$message.error('模型保存失败！');
                        } else if (response.data.status == 1) {
                            this.$message.success('模型保存成功！');
                            this.$router.push("/dashboard/workspace/project/" + this.$route.params.project_id + "/model");
                        } else {
                            this.$message.error('非法状态！');
                        }
                    });
                }
            })
        },

        // 切换标签
        onTabChange(key, type) {
            console.log(key, type);
            this[type] = key;
        },
    }
}
</script>
