import { API_BASE_URL } from "@/config/api.ts";

/**
 * Submits a rating for a specific recommendation submission.
 * @param submissionId - The ID of the submission to rate.
 * @param rating - Integer between 1 and 5.
 */
export async function rateRecommendationEndpoint(submissionId: number, rating: number) {
  const response = await fetch(`${API_BASE_URL}/recommendation/${submissionId}/submit?rating=${rating}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    }
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || `Error ${response.status}: Failed to submit rating`);
  }

  return await response.json();
}