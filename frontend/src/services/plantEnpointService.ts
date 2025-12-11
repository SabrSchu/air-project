import { API_BASE_URL } from "@/config/api.ts";

export async function accessPlantsEndpoint(skip = 0, limit = 600) {
    const response = await fetch(`${API_BASE_URL}/plants/all?skip=${skip}&limit=${limit}`);
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