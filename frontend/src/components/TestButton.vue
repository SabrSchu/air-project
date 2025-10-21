<!-- Simple Button just for testing accessing the Endpoints -->

<template>
  <div style="display: flex; flex-direction: column; align-items: center;">
    <button @click="fetchData" style="padding: 10px 20px; font-size: 16px;">
      Call Test Endpoint
    </button>

    <pre v-if="response" style="margin-top: 20px; text-align: left;">
{{ response }}
    </pre>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { accessTestEndpoint } from '../services/testEndpointsService.ts'

const response = ref<string | null>(null)

/**
 * Function that calls the services which call our Backend endpoints
 */
async function fetchData() {
  try {
    const data = await accessTestEndpoint()
    response.value = JSON.stringify(data, null, 2)
  } catch (err) {
    response.value = `Error: You must run the API first!`
  }
}
</script>