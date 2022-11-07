<script>
export default {
  data() {
    return {
      mode: "currentLocation",
      customLocationText: '',
      customLocation: {
        lat: 0,
        lng: 0
      },
    }
  },
  methods: {
    async getPosition() {
      if (this.mode === "currentLocation") {
        try {
          const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
          });
          return {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
        } catch (error) {
          alert(error.message);
        }
      } else {
        alert("TODO");
      }
    }
  }
};
</script>

<template>
  <div>
    <div class="form-check">
      <input class="form-check-input" type="radio" id="currentLocation" v-model="mode" value="currentLocation" />
      <label class="form-check-label" for="currentLocation">使用当前位置</label>
    </div>
    <div class="form-check">
      <input class="form-check-input" type="radio" id="customLocation" v-model="mode" value="customLocation" />
      <input type="text" :disabled="mode != 'customLocation'" v-model="customLocationText" placeholder="指定地址" />
    </div>
    <button @click="getPosition">搜索窝窝</button>
  </div>
</template>

<style>

</style>
