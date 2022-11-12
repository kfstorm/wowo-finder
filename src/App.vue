<script>
import QueryComposer from "./components/QueryComposer.vue";
import WowoPreview from "./components/WowoPreview.vue";
import wowoApi from "./wowoApi.js";

export default {
  components: {
    QueryComposer,
    WowoPreview,
  },
  data() {
    return {
      siteList: [],
      searchState: 0,
      allStats: {},
      searchAddress: "",
    };
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
    },
  },
};
</script>

<template>
  <div class="head">
    <h1 class="title">🚗 找窝窝</h1>
    <QueryComposer @location-found="onLocationFound" />
    <div v-if="searchState === 1">
      <p>
        在
        <span class="address">{{ searchAddress }}</span>
        附近搜索中……
      </p>
    </div>
    <div v-if="searchState === 2">
      <p>
        在
        <span class="address">{{ searchAddress }}</span>
        附近共找到
        <span class="count">{{ siteList.length }}</span>
        个结果
      </p>
    </div>
  </div>
  <WowoPreview
    v-for="site in siteList"
    :key="site.siteId"
    :site-id="site.siteId"
    @received-stats="onReceivedStats"
  />
</template>

<style>
.head {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.title {
  font-size: 3em;
  color: greenyellow;
}

.count,
.address {
  color: lightgreen;
  font-weight: bold;
}
</style>
