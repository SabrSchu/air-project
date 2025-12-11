import { API_BASE_URL } from "@/config/api.ts";

export async function accessPlantsEndpoint() {
    const response = await fetch(`${API_BASE_URL}/plants/all?skip=0&limit=10`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

export async function filterPlantsByName(name: string) {
    const url = new URL(`${API_BASE_URL}/plants/filter`);
    url.searchParams.append("name", name);

    const response = await fetch(url.toString());
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}