<script>
import Query from './components/Query.vue';
import WowoPreview from './components/WowoPreview.vue';
import wowoApi from './wowoApi.js';

export default {
  components: {
    Query,
    WowoPreview,
  },
  data() {
    return {
      siteList: [],
      searchState: 0,
      allStats: {},
      searchAddress: "",
    }
  },

  methods: {
    async onLocationFound(location) {
      this.searchState = 1;
      this.searchAddress = location.address;
      try {
        this.siteList = await wowoApi.getWowoList(location.lat, location.lng);
      } catch (e) {
        alert(e.message);
        this.searchState = 0;
        return;
      }
      this.searchState = 2;
      this.sortSites();
    },
    getFavorites(site) {
      if (this.allStats[site.siteId]) {
        return this.allStats[site.siteId].favorites;
      } else {
        return 0;
      }
    },
    sortSites() {
      this.siteList.sort((a, b) => {
        return this.getFavorites(b) - this.getFavorites(a);
      });
    },
    onReceivedStats({ siteId, stats }) {
      this.allStats[siteId] = stats;
      this.sortSites();
    }
  }
}

</script>

<template>
  <div class="main">
    <div class="title main-items">
      🚗 找窝窝
    </div>
    <Query class="main-items" @location-found="onLocationFound" />
    <div class="main-items" v-if="searchState === 1">
      <p class="searchStatus">在{{searchAddress}}附近搜索中……</p>
    </div>
    <div class="main-items" v-if="searchState === 2">
      <p class="searchStatus">在{{searchAddress}}附近共找到<span class="count">{{ siteList.length }}</span>个结果</p>
    </div>
    <WowoPreview class="main-items" v-for="site in siteList" :key="site.siteId" :site-id="site.siteId" @received-stats="onReceivedStats" />
  </div>
</template>

<style>
.main {
  margin-top: 50px;
}

.main-items {
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
