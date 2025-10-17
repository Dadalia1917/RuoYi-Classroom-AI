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
      <el-form-item label="检测结果" prop="label">
        <el-input
          v-model="queryParams.label"
          placeholder="请输入检测结果"
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
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['ai:imgRecords:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['ai:imgRecords:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['ai:imgRecords:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['ai:imgRecords:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="recordList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="ID" align="center" prop="id" />
      <el-table-column label="用户名" align="center" prop="username" />
      <el-table-column label="检测模型" align="center" prop="weight" />
      <el-table-column label="输入图片" align="center" prop="inputImg">
        <template #default="scope">
          <el-image
            v-if="scope.row.inputImg"
            :src="scope.row.inputImg"
            :preview-src-list="[scope.row.inputImg]"
            style="width: 50px; height: 50px"
            fit="cover"
          />
        </template>
      </el-table-column>
      <el-table-column label="输出图片" align="center" prop="outImg">
        <template #default="scope">
          <el-image
            v-if="scope.row.outImg"
            :src="scope.row.outImg"
            :preview-src-list="[scope.row.outImg]"
            style="width: 50px; height: 50px"
            fit="cover"
          />
        </template>
      </el-table-column>
      <el-table-column label="置信度" align="center" prop="confidence" />
      <el-table-column label="总耗时" align="center" prop="allTime" />
      <el-table-column label="检测结果" align="center" prop="label" width="200">
        <template #default="scope">
          <span>{{ formatLabel(scope.row.label) }}</span>
        </template>
      </el-table-column>
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
            v-hasPermi="['ai:imgRecords:query']"
          >查看</el-button>
          <el-button
            type="text"
            icon="Edit"
            @click="handleUpdate(scope.row)"
            v-hasPermi="['ai:imgRecords:edit']"
          >修改</el-button>
          <el-button
            type="text"
            icon="Delete"
            @click="handleDelete(scope.row)"
            v-hasPermi="['ai:imgRecords:remove']"
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

    <!-- 添加或修改图片记录对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="检测模型" prop="weight">
          <el-input v-model="form.weight" placeholder="请输入检测模型" />
        </el-form-item>
        <el-form-item label="置信度" prop="confidence">
          <el-input v-model="form.confidence" placeholder="请输入置信度" />
        </el-form-item>
        <el-form-item label="检测结果" prop="label">
          <el-input v-model="form.label" placeholder="请输入检测结果" />
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

    <!-- 查看详情对话框 -->
    <el-dialog title="图片记录详情" v-model="viewOpen" width="80%" append-to-body>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="ID">{{ viewData.id }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ viewData.username }}</el-descriptions-item>
        <el-descriptions-item label="检测模型">{{ viewData.weight }}</el-descriptions-item>
        <el-descriptions-item label="置信度">{{ viewData.confidence }}</el-descriptions-item>
        <el-descriptions-item label="总耗时">{{ viewData.allTime }}</el-descriptions-item>
        <el-descriptions-item label="检测结果">{{ formatLabel(viewData.label) }}</el-descriptions-item>
        <el-descriptions-item label="AI助手">{{ viewData.ai }}</el-descriptions-item>
        <el-descriptions-item label="检测时间">{{ parseTime(viewData.startTime) }}</el-descriptions-item>
      </el-descriptions>
      
      <div style="margin-top: 20px;">
        <h4>输入图片</h4>
        <el-image
          v-if="viewData.inputImg"
          :src="viewData.inputImg"
          :preview-src-list="[viewData.inputImg]"
          style="width: 300px; height: 200px; margin: 10px;"
          fit="contain"
        />
        
        <h4>输出图片</h4>
        <el-image
          v-if="viewData.outImg"
          :src="viewData.outImg"
          :preview-src-list="[viewData.outImg]"
          style="width: 300px; height: 200px; margin: 10px;"
          fit="contain"
        />
      </div>
      
      <div v-if="viewData.suggestion" style="margin-top: 20px;">
        <h4>AI建议</h4>
        <div class="suggestion-content" v-html="viewData.suggestion"></div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup name="ImgRecords">
import { listImgRecords, getImgRecords, delImgRecords, addImgRecords, updateImgRecords } from "@/api/ai/imgRecords";
import { parseTime } from "@/utils/ruoyi";

const { proxy } = getCurrentInstance();

const recordList = ref([]);
const open = ref(false);
const viewOpen = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const dateRange = ref([]);

const data = reactive({
  form: {},
  viewData: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    username: null,
    label: null,
    startTime: null
  },
  rules: {
    username: [
      { required: true, message: "用户名不能为空", trigger: "blur" }
    ],
    weight: [
      { required: true, message: "检测模型不能为空", trigger: "blur" }
    ]
  }
});

const { queryParams, form, rules, viewData } = toRefs(data);

/** 查询图片记录列表 */
function getList() {
  loading.value = true;
  queryParams.value.params = {};
  if (null != dateRange && '' != dateRange && dateRange.value) {
    queryParams.value.params["beginTime"] = dateRange.value[0];
    queryParams.value.params["endTime"] = dateRange.value[1];
  }
  listImgRecords(queryParams.value).then(response => {
    recordList.value = response.data || [];
    total.value = recordList.value.length;
    loading.value = false;
  }).catch(() => {
    recordList.value = [];
    total.value = 0;
    loading.value = false;
  });
}

// 取消按钮
function cancel() {
  open.value = false;
  reset();
}

// 表单重置
function reset() {
  form.value = {
    id: null,
    username: null,
    weight: null,
    inputImg: null,
    outImg: null,
    confidence: null,
    allTime: null,
    conf: null,
    label: null,
    startTime: null,
    ai: null,
    suggestion: null
  };
  proxy.resetForm("formRef");
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
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加图片记录";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const id = row.id || ids.value
  getImgRecords(id).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改图片记录";
  });
}

/** 查看按钮操作 */
function handleView(row) {
  viewData.value = row;
  viewOpen.value = true;
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["formRef"].validate(valid => {
    if (valid) {
      if (form.value.id != null) {
        updateImgRecords(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addImgRecords(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const delIds = row.id || ids.value;
  proxy.$modal.confirm('是否确认删除图片记录编号为"' + delIds + '"的数据项？').then(function() {
    return delImgRecords(delIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('ai/imgRecords/export', {
    ...queryParams.value
  }, `img_records_${new Date().getTime()}.xlsx`)
}

// 行为标签映射（英文 -> 中文）
const behaviorMap = {
  'Writing': '写作',
  'Reading': '阅读',
  'Listening': '听讲',
  'Sleeping': '睡觉',
  'Discussing': '讨论',
  'Raising_hand': '举手',
  'Bowing': '低头',
  'Phone': '玩手机',
  'Stand': '站立'
}

// 格式化标签（英文转中文，保留所有标签不去重）
function formatLabel(label) {
  if (!label) return '-'
  
  let labels = []
  if (typeof label === 'string') {
    try {
      // 先尝试JSON解析（会自动解码 \uXXXX）
      const parsed = JSON.parse(label)
      if (Array.isArray(parsed)) {
        labels = parsed
      } else {
        labels = [parsed]
      }
      console.log('JSON.parse成功:', label, '→', labels)
    } catch (e) {
      console.warn('JSON.parse失败:', label, e.message)
      // 如果解析失败，可能是双重转义，尝试处理
      try {
        // 替换双重转义的反斜杠
        const unescaped = label.replace(/\\\\u/g, '\\u')
        const parsed2 = JSON.parse(unescaped)
        if (Array.isArray(parsed2)) {
          labels = parsed2
        } else {
          labels = [parsed2]
        }
        console.log('二次解析成功:', unescaped, '→', labels)
      } catch (e2) {
        console.warn('二次解析也失败，使用原字符串:', e2.message)
        labels = [label]
      }
    }
  } else if (Array.isArray(label)) {
    labels = label
    console.log('label已经是数组:', labels)
  } else {
    return '-'
  }

  // 翻译成中文（不去重，保留所有标签）
  const translatedLabels = []
  labels.forEach(l => {
    if (!l) return
    
    let labelStr = String(l)
    
    // 匹配英文标签并翻译
    let translated = false
    for (const [en, cn] of Object.entries(behaviorMap)) {
      if (labelStr.includes(en)) {
        translatedLabels.push(cn)
        translated = true
        break
      }
    }
    
    // 如果没有匹配到英文标签，检查是否已经是中文
    if (!translated && labelStr) {
      // 检查是否在behaviorMap的值中
      const isChineseLabel = Object.values(behaviorMap).includes(labelStr)
      if (isChineseLabel) {
        translatedLabels.push(labelStr)
      } else {
        // 不是已知标签，直接显示（可能是乱码或未知标签）
        console.warn('未识别的标签:', labelStr)
        translatedLabels.push(labelStr)
      }
    }
  })

  const result = translatedLabels.length > 0 ? translatedLabels.join(', ') : '-'
  console.log('formatLabel最终结果:', label, '→', result)
  return result
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
