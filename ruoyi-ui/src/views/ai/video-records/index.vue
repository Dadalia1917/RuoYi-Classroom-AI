<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="queryParams.username"
          placeholder="请输入用户名"
          clearable
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="检测时间">
        <el-date-picker
          v-model="dateRange"
          type="datetimerange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD HH:mm:ss"
          value-format="YYYY-MM-DD HH:mm:ss"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['ai:videoRecords:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['ai:videoRecords:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="recordList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" />
      <el-table-column label="用户名" align="center" prop="username" />
      <el-table-column label="检测模型" align="center" prop="weight" />
      <el-table-column label="输入视频" align="center" prop="inputVideo">
        <template #default="scope">
          <el-button
            v-if="scope.row.inputVideo"
            type="text"
            @click="handlePlayVideo(scope.row.inputVideo)"
          >播放输入视频</el-button>
        </template>
      </el-table-column>
      <el-table-column label="输出视频" align="center" prop="outVideo">
        <template #default="scope">
          <el-button
            v-if="scope.row.outVideo"
            type="text"
            @click="handlePlayVideo(scope.row.outVideo)"
          >播放输出视频</el-button>
        </template>
      </el-table-column>
      <el-table-column label="置信度" align="center" prop="conf" />
      <el-table-column label="检测时间" align="center" prop="startTime" width="180">
        <template #default="scope">
          <span>{{ parseTime(scope.row.startTime, '{y}-{m}-{d} {h}:{i}:{s}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="AI助手" align="center" prop="ai" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button
            type="text"
            icon="View"
            @click="handleView(scope.row)"
            v-hasPermi="['ai:videoRecords:query']"
          >查看</el-button>
          <el-button
            type="text"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['ai:videoRecords:edit']"
          >修改</el-button>
          <el-button
            type="text"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['ai:videoRecords:remove']"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 查看详情对话框 -->
    <el-dialog title="视频记录详情" v-model="viewOpen" width="80%" append-to-body>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="ID">{{ viewData.id }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ viewData.username }}</el-descriptions-item>
        <el-descriptions-item label="检测模型">{{ viewData.weight }}</el-descriptions-item>
        <el-descriptions-item label="置信度">{{ viewData.conf }}</el-descriptions-item>
        <el-descriptions-item label="AI助手">{{ viewData.ai }}</el-descriptions-item>
        <el-descriptions-item label="检测时间">{{ parseTime(viewData.startTime) }}</el-descriptions-item>
      </el-descriptions>
      
      <div style="margin-top: 20px;" v-if="viewData.inputVideo">
        <h4>输入视频</h4>
        <video :src="viewData.inputVideo" controls style="width: 400px; height: 300px;"></video>
      </div>
      
      <div style="margin-top: 20px;" v-if="viewData.outVideo">
        <h4>输出视频</h4>
        <video :src="viewData.outVideo" controls style="width: 400px; height: 300px;"></video>
      </div>
      
      <div v-if="viewData.suggestion" style="margin-top: 20px;">
        <h4>AI建议</h4>
        <div class="suggestion-content" v-html="viewData.suggestion"></div>
      </div>
    </el-dialog>

    <!-- 视频播放对话框 -->
    <el-dialog title="视频播放" v-model="videoOpen" width="70%" append-to-body>
      <div style="text-align: center;">
        <video :src="currentVideoUrl" controls style="max-width: 100%; max-height: 60vh;"></video>
      </div>
    </el-dialog>

    <!-- 修改视频记录对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="检测模型" prop="weight">
          <el-input v-model="form.weight" placeholder="请输入检测模型" />
        </el-form-item>
        <el-form-item label="置信度" prop="conf">
          <el-input v-model="form.conf" placeholder="请输入置信度" />
        </el-form-item>
        <el-form-item label="AI助手" prop="ai">
          <el-input v-model="form.ai" placeholder="请输入AI助手" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="VideoRecords">
import { listVideoRecords, getVideoRecords, delVideoRecords, updateVideoRecords } from "@/api/ai/videoRecords";
import { parseTime } from "@/utils/ruoyi";

const { proxy } = getCurrentInstance();

const recordList = ref([]);
const viewOpen = ref(false);
const videoOpen = ref(false);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const dateRange = ref([]);
const currentVideoUrl = ref('');

const data = reactive({
  form: {},
  viewData: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    username: null,
    startTime: null
  },
  rules: {
    username: [
      { required: true, message: "用户名不能为空", trigger: "blur" }
    ]
  }
});

const { form, queryParams, viewData, rules } = toRefs(data);

/** 查询视频记录列表 */
function getList() {
  loading.value = true;
  queryParams.value.params = {};
  if (null != dateRange && '' != dateRange && dateRange.value) {
    queryParams.value.params["beginTime"] = dateRange.value[0];
    queryParams.value.params["endTime"] = dateRange.value[1];
  }
  listVideoRecords(queryParams.value).then(response => {
    recordList.value = response.data || [];
    total.value = recordList.value.length;
    loading.value = false;
  }).catch(() => {
    recordList.value = [];
    total.value = 0;
    loading.value = false;
  });
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  dateRange.value = [];
  proxy.resetForm("queryRef");
  handleQuery();
}

// 多选框选中数据
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id);
  single.value = selection.length !== 1;
  multiple.value = !selection.length;
}

/** 表单重置 */
function reset() {
  form.value = {
    id: null,
    username: null,
    weight: null,
    inputVideo: null,
    outVideo: null,
    conf: null,
    ai: null,
    startTime: null,
    suggestion: null
  };
  proxy.resetForm("formRef");
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 查看按钮操作 */
function handleView(row) {
  viewData.value = row;
  viewOpen.value = true;
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const id = row.id || ids.value;
  getVideoRecords(id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改视频记录";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["formRef"].validate(valid => {
    if (valid) {
      updateVideoRecords(form.value).then(response => {
        proxy.$modal.msgSuccess("修改成功");
        open.value = false;
        getList();
      });
    }
  });
}

/** 播放视频 */
function handlePlayVideo(videoUrl) {
  currentVideoUrl.value = videoUrl;
  videoOpen.value = true;
}

/** 删除按钮操作 */
function handleDelete(row) {
  const delIds = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除视频记录编号为"' + delIds + '"的数据项？').then(function() {
    return delVideoRecords(delIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('ai/videoRecords/export', {
    ...queryParams.value
  }, `video_records_${new Date().getTime()}.xlsx`)
}

getList();
</script>

<style scoped>
.suggestion-content {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
}
</style>
