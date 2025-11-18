import {API_BASE_URL} from "@/config/api.ts";

export async function accessQuestionsEndpoint() {
    const response = await fetch(`${API_BASE_URL}/questions/all`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}