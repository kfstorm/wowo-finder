<script setup>
import Query from './components/Query.vue';
import wowoApi from './wowoApi.js';

// TODO: remove this.
async function onLocationFound(location) {
  alert(JSON.stringify(location));
  const data = await wowoApi.getWowoList(location.lat, location.lng);
  console.log(data);
}
</script>

<template>
  <div class="main">
    <Query @locationFound="onLocationFound"/>
  </div>
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
