<script setup>
import { ref } from 'vue';
import Query from './components/Query.vue';
import WowoPreview from './components/WowoPreview.vue';
import wowoApi from './wowoApi.js';

const siteList = ref([]);

const searchState = ref(0);

// TODO: remove this.
async function onLocationFound(location) {
  searchState.value = 1;
  try {
    siteList.value = await wowoApi.getWowoList(location.lat, location.lng);
  } catch (e) {
    alert(e.message);
    searchState.value = 0;
    return;
  }
  searchState.value = 2;
}
</script>

<template>
  <div class="main">
    <Query @location-found="onLocationFound" />
  </div>
  <div v-if="searchState === 1">
    <p>搜索中……</p>
  </div>
  <div v-if="searchState === 2">
    <p>共找到{{ siteList.length }}个结果</p>
  </div>
  <WowoPreview v-for="site in siteList" :key="site.siteId" :site-id="site.siteId" />
</template>

<style scoped>
.main {
  display: flex;
  justify-content: center;
  /* align-items: top; */
  /* height: 100vh; */
  margin-top: 10vh;
}
</style>
