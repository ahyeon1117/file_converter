import { ref } from "vue";
import axios from "axios";

export function useUpload(clientId) {
  const progress = ref(0);
  let ws = null;

  const uploadFiles = async (files, convertType) => {
    if (!files || files.length === 0) return;
    
    // WebSocket 연결
    ws = new WebSocket(`ws://localhost:8000/progress/${clientId}`);

    ws.onmessage = (event) => {
      const receivedProgress = Number(event.data);
      progress.value = receivedProgress;

      if (receivedProgress >= 100) {
        ws?.close();
      }
    };

    try {
      // FormData 구성
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append("file", files[i]);
        // 파일 업로드 요청
        const response = await axios.post(
          `http://localhost:8000/convert?convert_type=${convertType}&client_id=${clientId}`,
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
            responseType: "blob", // 응답을 blob으로 받음
          }
        );
        const disposition = response.headers["content-disposition"];
        let filename = "converted_file"; // 기본 파일명
        console.log(disposition)
        if (disposition) {
          const filenameRegex = /filename\*=UTF-8''([^;]+)/i;
          const matches = disposition.match(filenameRegex);
          if (matches && matches[1]) {
            filename = decodeURIComponent(matches[1]);
          }
        }
        
        const blob = new Blob([response.data], { type: "application/octet-stream" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = filename; // 동적으로 파일명 설정
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }

    } catch (error) {
      console.error("File upload failed:", error);
    } finally {
      ws?.close();
    }
  };

  return { progress, uploadFiles };
}