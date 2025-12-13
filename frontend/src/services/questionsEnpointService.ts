import { API_BASE_URL } from "@/config/api.ts";

export async function accessQuestionsEndpoint() {
    const response = await fetch(`${API_BASE_URL}/questions/all`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

interface AnswerPayload {
    answers: { question_id: number; answer_id: number }[];
    created_at: string;
    free_text: string;
}

interface RecommendationParams {
    num_perfect_fits?: number;
    num_good_fits?: number;
    num_bad_fits?: number;
}

/**
 * Sends the user's completed questionnaire to the backend to receive plant recommendations.
 * @param questionnaireData The user's answers and free text.
 * @param params Optional parameters to control the number of recommendations.
 */
export async function postQuestionnaire(
    questionnaireData: AnswerPayload,
    params: RecommendationParams = {}
) {
    const query = new URLSearchParams({
        num_perfect_fits: params.num_perfect_fits?.toString() ?? '3',
        num_good_fits: params.num_good_fits?.toString() ?? '3',
        num_bad_fits: params.num_bad_fits?.toString() ?? '3',
    }).toString();

    const response = await fetch(`${API_BASE_URL}/questions/?${query}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(questionnaireData),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail}`);
    }
    return await response.json();
}

interface UserFreeTextPayload {
    created_at: string;
    free_text: string;
}

interface RecommendationParams {
    num_perfect_fits?: number;
    num_good_fits?: number;
    num_bad_fits?: number;
}

/**
 * Sends user free text to receive plant recommendations.
 * @param freeText The user's free text.
 * @param params Optional parameters to control the number of recommendations.
 */
export async function postFreeText(
    freeText: UserFreeTextPayload,
    params: RecommendationParams = {}
) {
    const query = new URLSearchParams({
        num_perfect_fits: params.num_perfect_fits?.toString() ?? '3',
        num_good_fits: params.num_good_fits?.toString() ?? '3',
        num_bad_fits: params.num_bad_fits?.toString() ?? '3',
    }).toString();

    const response = await fetch(`${API_BASE_URL}/questions/free_text?${query}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(freeText),
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.detail}`);
    }

    return await response.json();
}

export async function getUserStudyQuestions() {
    const response = await fetch(`${API_BASE_URL}/user_study/questions`);
    if (!response.ok) throw new Error("Failed to fetch user study questions");
    return await response.json();
}

export async function submitUserStudy(submission: any) {
    const response = await fetch(`${API_BASE_URL}/user_study/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(submission),
    });
    if (!response.ok) throw new Error("Failed to submit user study");
    return await response.json();
}
