<script setup lang="ts">
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart, LineChart, PieChart } from 'echarts/charts';
import { GridComponent, TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { ref, computed } from 'vue';

use([
  CanvasRenderer,
  BarChart, LineChart, PieChart,
  GridComponent, TitleComponent, TooltipComponent, LegendComponent
]);

const props = defineProps<{
  options: Record<string, any>
}>();

const chartOptions = computed(() => ({
  ...props.options,
  backgroundColor: 'transparent',
}));
</script>

<template>
  <div class="chart-container">
    <v-chart class="chart" :option="chartOptions" autoresize />
  </div>
</template>

<style scoped>
.chart-container {
  height: 400px;
  width: 100%;
  border-radius: 8px;
  background-color: #f9f9f9;
  padding: 16px;
  box-sizing: border-box;
}
.chart {
  height: 100%;
  width: 100%;
}
</style>
