<script setup lang="ts">
import { ref } from 'vue';
import { NConfigProvider, NMessageProvider, NGlobalStyle, NLayout, NLayoutHeader, NLayoutContent, NSpace, NText, NButton, NIcon } from 'naive-ui';
import { ArrowBack as BackIcon } from '@vicons/ionicons5';
import FileUpload from './components/FileUpload.vue';
import ChatInterface from './components/ChatInterface.vue';
import type { UploadResponse } from './api';

const currentFile = ref<UploadResponse | null>(null);

const handleUploadSuccess = (data: UploadResponse) => {
  currentFile.value = data;
};

const resetSession = () => {
  currentFile.value = null;
};
</script>

<template>
  <n-config-provider>
    <n-global-style />
    <n-message-provider>
      <n-layout style="height: 100vh">
        <n-layout-header bordered style="padding: 16px 32px; display: flex; align-items: center; justify-content: space-between;">
          <n-text h2 style="margin: 0; font-weight: bold; font-size: 24px;">
            Mini Chat BI 🤖
          </n-text>
          
          <n-button v-if="currentFile" text @click="resetSession">
            <template #icon>
              <n-icon><back-icon /></n-icon>
            </template>
            上传新文件
          </n-button>
        </n-layout-header>
        
        <n-layout-content content-style="padding: 24px; max-width: 900px; margin: 0 auto;">
          <transition name="fade" mode="out-in">
            <!-- 场景 1: 上传文件 -->
            <n-space v-if="!currentFile" vertical size="large">
              <div style="margin-bottom: 20px;">
                <n-text depth="3">
                  简单好用的数据分析助手。上传 Excel 表格，通过对话获取洞察。
                </n-text>
              </div>
              <FileUpload @upload-success="handleUploadSuccess" />
            </n-space>

            <!-- 场景 2: 对话分析 -->
            <ChatInterface 
              v-else 
              :file-id="currentFile.id" 
              :file-name="currentFile.filename"
            />
          </transition>
        </n-layout-content>
      </n-layout>
    </n-message-provider>
  </n-config-provider>
</template>

<style>
body {
  margin: 0;
  font-family: v-sans, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
