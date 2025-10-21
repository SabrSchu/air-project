import { API_BASE_URL } from '../config/api';

/**
 * Small method accessing the api test endpoint and displaying the raw json response
 * --> only for testing of initial project setup
 */
export async function accessTestEndpoint() {
    const response = await fetch(`${API_BASE_URL}/test`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}


/**
 * Method for accessing the data endpoint and displaying the raw json response
 *  --> only for testing of initial project setup
 */
export async function accessDataEndpoint() {
    const response = await fetch(`${API_BASE_URL}/data/columns`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}