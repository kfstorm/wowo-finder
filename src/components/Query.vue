<script>
export default {
  data() {
    return {
      mode: "currentLocation",
      loading: false,
      customLocationText: '',
      customLocation: {
        lat: 0,
        lng: 0
      },
    }
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
              lng: position.coords.longitude
            };
            this.$emit('locationFound', ret);
          } catch (error) {
            alert("无法获取当前位置。");
            console.error(error);
          }
        } else {
          alert("TODO");
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<template>
  <div>
    <div>
      <input type="radio" id="currentLocation" v-model="mode" value="currentLocation" />
      <label for="currentLocation">使用当前位置</label>
    </div>
    <div>
      <input type="radio" id="customLocation" v-model="mode" value="customLocation" />
      <input type="text" :disabled="mode != 'customLocation'" v-model="customLocationText" placeholder="指定地址" />
    </div>
    <button @click="getPosition">{{loading ? '获取位置中……' : '搜索窝窝'}}</button>
  </div>
</template>

<style>

</style>
