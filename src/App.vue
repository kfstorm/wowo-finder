<script setup>
import { ref } from 'vue';
import Query from './components/Query.vue';
import WowoPreview from './components/WowoPreview.vue';
import wowoApi from './wowoApi.js';

const siteList = ref([]);

const searchState = ref(0);

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

function sortSites() {
  siteList.value.sort((a, b) => {
    return (b.stats ? b.stats.favorites : 0) - (a.stats ? a.stats.favorites: 0);
  });
}

function onReceivedStats({ siteId, stats }) {
  const site = siteList.value.find(site => site.siteId == siteId);
  site.stats = stats;

  sortSites();
}

</script>

<template>
  <div class="main">
    <Query @location-found="onLocationFound" />
    <div v-if="searchState === 1">
      <p class="searchStatus">搜索中……</p>
    </div>
    <div v-if="searchState === 2">
      <p class="searchStatus">共找到<span class="count">{{ siteList.length }}</span>个结果</p>
    </div>
    <WowoPreview v-for="site in siteList" :key="site.siteId" :site-id="site.siteId" @received-stats="onReceivedStats"/>
  </div>
</template>

<style scoped>
.main {
  margin-top: 50px;
}

.main * {
  margin: 0 auto;
  width: fit-content;
}

.searchStatus {
  margin: 10px 0;
}

.count {
  color: lightgreen;
  font-weight: bold;
  margin: 0 5px;
}
</style>
