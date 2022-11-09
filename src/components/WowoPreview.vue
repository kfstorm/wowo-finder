<script>
import wowoApi from "../wowoApi.js";

export default {
  data() {
    return {
      loading: true,
      uniqueToken: null,
      images: [],
      address: [],
      description: "",
      capabilities: {
        camping: {
          available: false,
          icon: "⛺️",
        },
        toilet: {
          available: false,
          icon: "🚾",
        },
      },
      style: "",
      favorites: 0,
      rewards: 0,
      shares: 0,
      rating: 0,
    };
  },
  props: {
    siteId: Number,
  },
  methods: {
    onClick() {
      window.open(
        `http://web.woyouzhijia.cn/web/share.html?${this.uniqueToken}`,
        "_blank"
      );
    },
    getCapabilityStyle(capability) {
      if (this.capabilities[capability].available) {
        return "";
      } else {
        return "filter: grayscale(100%)";
      }
    },
  },
  emits: ["receivedStats"],
  async mounted() {
    const wowo = await wowoApi.getWowo(this.siteId);
    this.loading = false;

    this.uniqueToken = wowo.subSite.uniqueToken;
    this.images = wowo.subSite.imageList;
    this.address = wowo.subSite.address;
    this.description = wowo.subSite.description;
    this.style = wowo.subSite.style;

    this.capabilities.camping.available = wowo.subSite.iconList.includes(24);
    this.capabilities.toilet.available = wowo.subSite.iconList.includes(25);

    this.favorites = wowo.countCollect;
    this.rewards = wowo.countReward;
    this.shares = wowo.countShare;
    this.rating = wowo.averageScore;

    this.$emit("receivedStats", {
      siteId: this.siteId,
      stats: {
        favorites: this.favorites,
        rewards: this.rewards,
        shares: this.shares,
        rating: this.rating,
      },
    });
  },
};
</script>

<template>
  <div>
    <p v-if="loading">加载中……</p>
    <div class="container" v-if="!loading" @click="onClick">
      <div class="mainPreview">
        <div>
          <img class="pic" :src="images[0]" />
          <div class="style">{{ style }}</div>
        </div>
        <div>
          <div class="description">{{ description }}</div>
          <div class="addressLine">
            <span class="pin">📍</span>
            <span>{{ address }}</span>
          </div>
          <div class="capability-list">
            <span
              v-for="({ icon }, key) in capabilities"
              :key="key"
              :style="getCapabilityStyle(key)"
              >{{ icon }}</span
            >
          </div>
        </div>
      </div>
      <div class="stats">
        <span>❤️ {{ favorites }}</span>
        <span>🪙 {{ rewards }}</span>
        <span>↗️ {{ shares }}</span>
        <span>⭐️ {{ rating }}</span>
      </div>
    </div>
  </div>
</template>

<style>
.container {
  margin: 10px;

  border-style: solid;
  border-color: lightgray;
  border-width: medium;
  border-radius: 5px;

  background-color: lavender;
}

.mainPreview {
  display: flex;
}

.pic {
  padding: 10px;
  object-fit: cover;
  width: 100px;
  height: 100px;
}

.capability-list {
  display: flex;
  gap: 0.5em;
  font-size: 2em;
}

.description {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  /* number of lines to show */
  -webkit-line-clamp: 4;
  line-clamp: 4;
  -webkit-box-orient: vertical;

  font-size: 0.8em;
  margin-top: 10px;
}

.style {
  text-align: center;
}

.pin {
  margin-right: 10px;
}

.addressLine {
  margin: 10px 0;
  font-size: 0.8em;
}

.stats * {
  margin-right: 10px;
}
</style>
