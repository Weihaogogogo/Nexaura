<template>
  <div class="element-plus-demo">
    <h2>Element Plus 组件示例</h2>
    
    <!-- 按钮组件 -->
    <div class="demo-section">
      <h3>按钮组件</h3>
      <el-button>默认按钮</el-button>
      <el-button type="primary">主要按钮</el-button>
      <el-button type="success">成功按钮</el-button>
      <el-button type="warning">警告按钮</el-button>
      <el-button type="danger">危险按钮</el-button>
    </div>

    <!-- 输入框组件 -->
    <div class="demo-section">
      <h3>输入框组件</h3>
      <el-input v-model="inputValue" placeholder="请输入内容" style="width: 300px;" />
      <p>输入内容: {{ inputValue }}</p>
    </div>

    <!-- 日期选择器 -->
    <div class="demo-section">
      <h3>日期选择器</h3>
      <el-date-picker
        v-model="dateValue"
        type="date"
        placeholder="选择日期"
        style="width: 300px;"
      />
      <p>选择日期: {{ dateValue }}</p>
    </div>

    <!-- 表格组件 -->
    <div class="demo-section">
      <h3>表格组件</h3>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="姓名" width="180" />
        <el-table-column prop="age" label="年龄" width="180" />
        <el-table-column prop="address" label="地址" />
      </el-table>
    </div>

    <!-- 消息提示 -->
    <div class="demo-section">
      <h3>消息提示</h3>
      <el-button @click="showMessage">显示消息</el-button>
      <el-button @click="showNotification">显示通知</el-button>
    </div>

    <!-- 图标示例 -->
    <div class="demo-section">
      <h3>图标示例</h3>
      <el-icon><Edit /></el-icon>
      <el-icon><Delete /></el-icon>
      <el-icon><Search /></el-icon>
      <el-icon><Setting /></el-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import { Edit, Delete, Search, Setting } from '@element-plus/icons-vue'

const inputValue = ref('')
const dateValue = ref('')

const tableData = ref([
  { name: '张三', age: 25, address: '北京市朝阳区' },
  { name: '李四', age: 30, address: '上海市浦东新区' },
  { name: '王五', age: 28, address: '广州市天河区' }
])

const showMessage = () => {
  ElMessage({
    message: '这是一条消息提示',
    type: 'success',
  })
}

const showNotification = () => {
  ElNotification({
    title: '成功',
    message: 'Element Plus 安装成功！',
    type: 'success',
  })
}
</script>

<style scoped>
.element-plus-demo {
  padding: 20px;
  max-width: 800px;
}

.demo-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
}

.demo-section h3 {
  margin-top: 0;
  color: #303133;
}

.el-button {
  margin-right: 10px;
  margin-bottom: 10px;
}

.el-icon {
  margin-right: 10px;
  font-size: 20px;
}
</style> 