<script setup>
import Query from './components/Query.vue';

// TODO: remove this.
function onLocationFound(location) {
  alert(JSON.stringify(location));
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
