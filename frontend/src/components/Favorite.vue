<template>
  <div>
    <!-- form here to add a new favorite-->
    <div class="fav-head row">
      <div class="col-1">Rank</div>
      <div class="col-4">Title</div>
      <div class="col-4">Date Added</div>
      <div class="col-3 action">Actions</div>
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
</style>
