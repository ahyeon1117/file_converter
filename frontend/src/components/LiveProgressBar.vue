<template>
  <div>
    <BarChart :chart-data="chartData" :chart-options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, watchEffect, defineProps } from "vue";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from "chart.js";
import { Bar } from "vue-chartjs";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

// ✅ 부모 컴포넌트에서 `progress` 값을 props로 받음
const props = defineProps({
  progress: Number
});

const chartData = ref({
  labels: ["Progress"],
  datasets: [
    {
      label: "Upload Progress",
      data: [props.progress], // 초기 값 설정
      backgroundColor: ["rgba(54, 162, 235, 0.5)"]
    }
  ]
});

const chartOptions = ref({
  responsive: true,
  scales: {
    y: {
      beginAtZero: true,
      max: 100
    }
  }
});

// ✅ props 값이 변경될 때 차트 데이터 업데이트
watchEffect(() => {
  chartData.value.datasets[0].data = [props.progress];
});
</script>

<style scoped>
h3 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
