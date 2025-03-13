<script setup lang="ts">
import { useClientId } from "@/utils/useClientId";
import { useUpload } from "@/utils/upload";
import { ref } from "vue";
import Chart from "@/components/LiveProgressBar.vue";

const { clientId } = useClientId(); // 고유한 clientId 생성
const { progress, uploadFiles } = useUpload(clientId.value);
const selectedFiles = ref<FileList | null>(null);
const convertType = ref<string>("png_to_pdf"); // 기본 변환 타입

const handleUpload = () => {
  if (selectedFiles.value) {
    uploadFiles(selectedFiles.value, convertType.value);
  }
};
</script>

<template>
  <div>
    <h3>Your Client ID: {{ clientId }}</h3>

    <label>
      Select Files:
      <input
        type="file"
        multiple
        @change="selectedFiles = $event.target.files"
      />
    </label>

    <label>
      Conversion Type:
      <select v-model="convertType">
        <option value="png_to_pdf">PNG to PDF</option>
        <option value="pdf_to_png">PDF to PNG</option>
      </select>
    </label>

    <button @click="handleUpload">Upload & Convert</button>

    <!-- <h3>Uploading... {{ progress }}%</h3> -->
    <chart :progress="progress" />
    <!-- <progress :value="progress" max="100"></progress> -->

    <!-- <h3 v-if="progress >= 100">Upload Complete!</h3> -->
  </div>
</template>

<style scoped>
progress {
  width: 100%;
  height: 10px;
}
</style>
