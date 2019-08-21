<template>
  <div>
    <!-- form here to add a new favorite-->
    <div class="fav-head row">
      <div class="col-lg-1 col-sm-4">Rank</div>
      <div class="col-lg-4 show">Title</div>
      <div class="col-lg-4 show">Date Added</div>
      <div class="col-lg-3 col-sm-8 action">Actions</div>
    </div>
    <div v-bind:key="favorite.id" v-for="favorite in favorites">
      <FavoriteItem
        v-bind:favorite="favorite"
        v-on:update-favorite="updateFavorite"
      />
    </div>
  </div>
</template>

<script>
import FavoriteItem from "./FavoriteItem.vue";
export default {
  name: "Favorites",
  components: {
    FavoriteItem
  },
  props: ["favorites"],
  methods: {
    updateFavorite() {
      this.$emit("update-favorite");
    }
  }
};
</script>

<style scoped>
.fav-head {
  background: rgb(21, 156, 235);
  padding: 10px;
  color: aliceblue;
  border-bottom: 1px #ccc dotted;
}
.show {
  display: block;
}
@media only screen and (min-device-width: 320px) and (max-device-width: 480px) {
  .show {
    display: none;
  }
}
</style>
