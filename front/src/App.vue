<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppNavBar from './components/common/AppNavBar.vue';
</script>

<template>
  <header>
    <nav>
      <AppNavBar />
      <RouterView />
    </nav>
  </header>
</template>


<style scoped>

</style>
