import { ref } from "vue";

export function useClientId() {
  const clientId = ref<string>(localStorage.getItem("clientId") || `${crypto.randomUUID()}-${Date.now()}`);

  // ID를 로컬 스토리지에 저장하여 유지
  localStorage.setItem("clientId", clientId.value);

  return { clientId };
}
