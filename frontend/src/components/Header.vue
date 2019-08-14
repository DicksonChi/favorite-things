<template>
  <header class="header">
    <h1>My List of Favorite Things</h1>
    <div id="nav" align="right">
      <router-link to="/" class="link"> Logout</router-link>
    </div>
  </header>
</template>

<script>
export default {
  name: "Header"
};
</script>

<style scoped>
.header {
  background: rgb(21, 156, 235);
  color: #fff;
  text-align: center;
  padding: 10px;
}
.link {
  color: white;
}
</style>
