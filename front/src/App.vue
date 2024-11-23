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


<style>
/* 전체 웹 페이지 배경을 노란색으로 설정 */
body {
  background-color: #F9EB87;
}
</style>
