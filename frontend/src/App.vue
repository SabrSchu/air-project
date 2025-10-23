<!-- Test Screen with some buttons to test accessing our Backend -->

<template>
  <div style="background-color: white; height: 100vh; display: flex; justify-content: center; align-items: center;">
    <TestButton />
    <DataButton />
  </div>
</template>

<script setup lang="ts">
import TestButton from './components/TestButton.vue'
import DataButton from './components/DataButton.vue'
</script>