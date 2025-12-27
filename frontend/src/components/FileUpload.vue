<script setup lang="ts">
import { ref, computed } from 'vue';
import { NUpload, NUploadDragger, NIcon, NText, NP, NDataTable, NCard, NSpace, NSpin, useMessage } from 'naive-ui';
import { ArchiveOutline as ArchiveIcon } from '@vicons/ionicons5';
import { uploadFile, type UploadResponse } from '../api';

import { type UploadCustomRequestOptions } from 'naive-ui';

const message = useMessage();
const loading = ref(false);
const uploadData = ref<UploadResponse | null>(null);

const emit = defineEmits<{
  (e: 'upload-success', data: UploadResponse): void
}>();

const handleUpload = async ({ file }: UploadCustomRequestOptions) => {
  if (!file.file) {
    message.error('无法获取文件对象');
    return;
  }
  
  loading.value = true;
  try {
    const res = await uploadFile(file.file);
    uploadData.value = res;
    message.success('文件上传成功！');
    emit('upload-success', res);
  } catch (error) {
    console.error(error);
    message.error('上传失败，请检查文件格式');
  } finally {
    loading.value = false;
  }
};

// 生成表格列配置
const columns = computed(() => {
  if (!uploadData.value) return [];
  return uploadData.value.columns.map(col => ({
    title: col,
    key: col
  }));
});
</script>

<template>
  <n-space vertical size="large">
    <!-- 上传区域 -->
    <n-upload
      v-if="!uploadData"
      directory-dnd
      :custom-request="handleUpload"
      :show-file-list="false"
      accept=".csv,.xlsx,.xls"
    >
      <n-upload-dragger>
        <div style="margin-bottom: 12px">
          <n-icon size="48" :depth="3">
            <archive-icon />
          </n-icon>
        </div>
        <n-text style="font-size: 16px">
          点击或拖拽文件到此处上传
        </n-text>
        <n-p depth="3" style="margin: 8px 0 0 0">
          支持 CSV、Excel 文件，数据不离本地 (MVP)
        </n-p>
      </n-upload-dragger>
    </n-upload>

    <!-- 加载状态 -->
    <div v-if="loading" style="text-align: center; padding: 20px;">
      <n-spin size="large" description="正在解析数据..." />
    </div>

    <!-- 数据预览 -->
    <n-card v-if="uploadData && !loading" title="数据预览">
      <template #header-extra>
        <n-text depth="3">{{ uploadData.filename }}</n-text>
      </template>
      <n-data-table
        :columns="columns"
        :data="uploadData.preview"
        :bordered="false"
        style="max-height: 400px"
      />
    </n-card>
  </n-space>
</template>
