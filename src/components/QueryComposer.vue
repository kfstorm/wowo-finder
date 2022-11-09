<script>
import amapApi from "../amapApi.js";

export default {
  data() {
    return {
      mode: "currentLocation",
      loading: false,
      customLocationText: "",
      customLocation: {
        lat: 0,
        lng: 0,
      },
    };
  },
  methods: {
    async getPosition() {
      this.loading = true;
      try {
        if (this.mode === "currentLocation") {
          try {
            const position = await new Promise((resolve, reject) => {
              navigator.geolocation.getCurrentPosition(resolve, reject);
            });
            const ret = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
              address: "当前位置",
            };
            this.$emit("locationFound", ret);
          } catch (error) {
            alert("无法获取当前位置。");
            console.error(error);
          }
        } else {
          const geoCode = await amapApi.getGeoCode(this.customLocationText);
          const [lng, lat] = geoCode.location.split(",").map(parseFloat);
          const ret = {
            lat,
            lng,
            address: geoCode.formatted_address,
          };
          this.$emit("locationFound", ret);
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<template>
  <div class="query-container">
    <div class="mode-selector">
      <div>
        <input
          type="radio"
          id="currentLocation"
          v-model="mode"
          value="currentLocation"
        />
        <label for="currentLocation">使用当前位置</label>
      </div>
      <div>
        <input
          type="radio"
          id="customLocation"
          v-model="mode"
          value="customLocation"
        />
        <input
          type="text"
          :disabled="mode != 'customLocation'"
          v-model="customLocationText"
          placeholder="指定地址"
        />
      </div>
    </div>
    <button @click="getPosition" :disabled="loading">
      {{ loading ? "获取位置中……" : "搜索窝窝" }}
    </button>
  </div>
</template>

<style>
.query-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.mode-selector {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

input {
  margin-right: 10px;
}

button {
  font-size: 1.2em;
}
</style>
