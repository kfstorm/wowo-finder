<script setup>
import { ref } from 'vue';
import Query from './components/Query.vue';
import WowoPreview from './components/WowoPreview.vue';
import wowoApi from './wowoApi.js';

const siteList = ref([]);

const searchState = ref(0);

const allStats = ref({});

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
  sortSites();
}

function sortSites() {
  siteList.value.sort((a, b) => {
    function getFavorites(site) {
      if (allStats.value[site.siteId]) {
        return allStats.value[site.siteId].favorites;
      } else {
        return 0;
      }
    }
    return getFavorites(b) - getFavorites(a);
  });
}

function onReceivedStats({ siteId, stats }) {
  allStats.value[siteId] = stats;

  sortSites();
}

</script>

<template>
  <div class="main">
    <div class="title">
      🚗 找窝窝
    </div>
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

.title {
  font-size: 3em;
  color: greenyellow;
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
