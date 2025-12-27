<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue';
import { NInput, NButton, NIcon, NSpace, NCard, NText, NScrollbar, NAvatar } from 'naive-ui';
import { Send as SendIcon, Person as UserIcon, HardwareChip as BotIcon } from '@vicons/ionicons5';
import { sendChat } from '../api';
import ChartRenderer from './ChartRenderer.vue';

const props = defineProps<{
  fileId: number;
  fileName: string;
}>();

interface Message {
  id: string;
  role: 'user' | 'assistant';
  type: 'text' | 'chart' | 'error';
  content: string;
  options?: any;
  loading?: boolean;
}

const inputValue = ref('');
const loading = ref(false);
const messages = ref<Message[]>([
  {
    id: 'init',
    role: 'assistant',
    type: 'text',
    content: `你好！我已经准备好分析 **${props.fileName}** 了。你可以问我关于这份数据的任何问题，比如“销售额最高的是哪个城市？”`
  }
]);

const scrollbarInst = ref<any>(null);

const scrollToBottom = () => {
  nextTick(() => {
    if (scrollbarInst.value) {
      scrollbarInst.value.scrollTo({ position: 'bottom', behavior: 'smooth' });
    }
  });
};

const handleSend = async () => {
  const query = inputValue.value.trim();
  if (!query || loading.value) return;

  // 1. 添加用户消息
  messages.value.push({
    id: Date.now().toString(),
    role: 'user',
    type: 'text',
    content: query
  });
  inputValue.value = '';
  scrollToBottom();

  // 2. 添加 AI 加载消息
  const aiMsgId = (Date.now() + 1).toString();
  messages.value.push({
    id: aiMsgId,
    role: 'assistant',
    type: 'text',
    content: '正在思考中...',
    loading: true
  });
  scrollToBottom();
  loading.value = true;

  try {
    // 3. 调用 API
    const res = await sendChat({
      file_id: props.fileId,
      query: query
    });

    // 4. 更新 AI 消息
    const index = messages.value.findIndex(m => m.id === aiMsgId);
    if (index !== -1) {
      messages.value[index] = {
        id: aiMsgId,
        role: 'assistant',
        type: res.type,
        content: res.content,
        options: res.options,
        loading: false
      };
    }
  } catch (error) {
    const index = messages.value.findIndex(m => m.id === aiMsgId);
    if (index !== -1) {
      messages.value[index] = {
        id: aiMsgId,
        role: 'assistant',
        type: 'error',
        content: '抱歉，分析过程中发生了错误，请稍后再试。',
        loading: false
      };
    }
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};
</script>

<template>
  <div class="chat-container">
    <!-- 消息列表 -->
    <div class="message-list">
      <n-scrollbar ref="scrollbarInst">
        <n-space vertical size="large" style="padding: 20px;">
          <div v-for="msg in messages" :key="msg.id" :class="['message-row', msg.role === 'user' ? 'message-right' : 'message-left']">
            <!-- 头像 -->
            <n-avatar round size="small" :style="{ backgroundColor: msg.role === 'user' ? '#18a058' : '#2080f0' }">
              <n-icon>
                <user-icon v-if="msg.role === 'user'" />
                <bot-icon v-else />
              </n-icon>
            </n-avatar>

            <!-- 消息气泡 -->
            <div class="message-content">
              <!-- 文本消息 -->
              <div v-if="msg.type === 'text' || msg.type === 'error'" :class="['bubble', msg.role, msg.type === 'error' ? 'error-bubble' : '']">
                {{ msg.content }}
                <span v-if="msg.loading" class="dot-loading">...</span>
              </div>

              <!-- 图表消息 -->
              <div v-else-if="msg.type === 'chart'" class="chart-wrapper">
                <n-text depth="3" style="font-size: 12px; margin-bottom: 8px; display: block;">
                  {{ msg.content }}
                </n-text>
                <ChartRenderer :options="msg.options" />
              </div>
            </div>
          </div>
        </n-space>
      </n-scrollbar>
    </div>

    <!-- 输入框 -->
    <div class="input-area">
      <n-input
        v-model:value="inputValue"
        type="textarea"
        :autosize="{ minRows: 1, maxRows: 4 }"
        placeholder="输入你的问题，例如：按城市统计销售额..."
        @keydown.enter.prevent="handleSend"
        :disabled="loading"
      />
      <n-button type="primary" :disabled="!inputValue.trim() || loading" @click="handleSend" style="margin-left: 12px; height: auto;">
        <template #icon>
          <n-icon><send-icon /></n-icon>
        </template>
      </n-button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 600px; /* 固定高度或者 100% */
  background: #fff;
  border: 1px solid #eee;
  border-radius: 8px;
}

.message-list {
  flex: 1;
  overflow: hidden;
  background-color: #f4f6f8;
}

.message-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message-right {
  flex-direction: row-reverse;
}

.message-content {
  max-width: 80%;
}

.bubble {
  padding: 10px 16px;
  border-radius: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.bubble.user {
  background-color: #e7f5ee; /* Green tint */
  color: #333;
  border-top-right-radius: 2px;
}

.bubble.assistant {
  background-color: #fff;
  color: #333;
  border-top-left-radius: 2px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.error-bubble {
  background-color: #fef0f0 !important;
  color: #f56c6c !important;
}

.chart-wrapper {
  background: #fff;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  width: 500px; /* 图表宽度 */
}

.input-area {
  padding: 16px;
  border-top: 1px solid #eee;
  display: flex;
  align-items: flex-end;
}

.dot-loading {
  animation: blink 1.5s infinite;
}

@keyframes blink {
  0% { opacity: 0.2; }
  50% { opacity: 1; }
  100% { opacity: 0.2; }
}
</style>
