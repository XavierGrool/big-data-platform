<template>
<a-layout>
    <a-layout-sider width="200" style="background: #fff">
    <div style="height:64px;padding-top:20px;">
        <a @click="returnToProjects" style="fontSize:24px;margin-left:88px">
            <a-icon type="left" />
        </a>
    </div>
    <a-menu
        mode="inline"
        :default-selected-keys="['1']"
        :selectedKeys="selected_keys"
        :style="{ height: '100%', borderRight: 0 }"
    >
        <a-menu-item key="1" @click="clickDataset">
            <a-icon type="container" />数据集
        </a-menu-item>
        <a-menu-item key="2" @click="clickModel">
            <a-icon type="setting" />模型管理
        </a-menu-item>
        <a-menu-item key="3" @click="clickPrediction">
            <a-icon type="area-chart" />预测分析
        </a-menu-item>
    </a-menu>
    </a-layout-sider>
    <router-view></router-view>
</a-layout>
</template>

<script>
export default {
    name: "Project",
    data() {
        return {
            selected_keys: ["1"],
        }
    },
    created() {
        console.log(this.$route.path);
        var patt_dataset = new RegExp("dataset");
        var patt_model = new RegExp("model");
        var patt_prediction = new RegExp("prediction");
        if (patt_dataset.test(this.$route.path)) {
            console.log("匹配到 dataset");
            this.selected_keys = ["1"]
        } else if (patt_model.test(this.$route.path)) {
            console.log("匹配到 model");
            this.selected_keys = ["2"]
        } else if (patt_prediction.test(this.$route.path)) {
            console.log("匹配到 prediction");
            this.selected_keys = ["3"];
        } else {
            console.log("啥也没匹配到");
        }
    },
    methods: {
        // 返回项目空间
        returnToProjects() {
            this.$router.push("/dashboard/workspace/projects")
        },

        // 点击 "数据集"
        clickDataset(e) {
            console.log(e.key);
            this.selected_keys = ["1"]
            this.$router.push("/dashboard/workspace/project/" + this.$route.params.id + "/dataset")
        },

        // 点击 "模型管理"
        clickModel(e) {
            console.log(e.key);
            this.selected_keys = ["2"]
            console.log(this.$route.params)
            this.$router.push("/dashboard/workspace/project/" + this.$route.params.id + "/model")
        },

        // 点击 "预测分析"
        clickPrediction(e) {
            console.log(e.key);
            this.selected_keys = ["3"]
            this.$router.push("/dashboard/workspace/project/" + this.$route.params.id + "/prediction")
        },
    }
}
</script>
