<template>
  <div>
    <!-- form here to add a new category-->
    <modal v-if="isAddCatModalVisible">
      <h3 slot="header" class="modal-title">
        Add Category to the List
      </h3>

      <div slot="body">
        <form @submit="SubmitAddCatModal">
          <div class="form-group">
            <label for="name">Name</label>
            <input
              type="text"
              class="form-control"
              placeholder="Category"
              id="name"
              v-model="name"
            />
          </div>
          <div class="form-group">
            <button type="submit" class="btn btn-outline-info">Add</button>
            <button
              type="button"
              class="btn btn-outline-info"
              @click="closeAddCatModal"
            >
              close
            </button>
          </div>
        </form>
      </div>
    </modal>
    <button
      class="btn btn-lg"
      title="add a new category"
      @click="showAddCatModal"
    >
      Add Category <i class="fa fa-plus"></i>
    </button>

    <div v-bind:key="category.id" v-for="category in categories">
      <CategoryItem v-bind:category="category" v-on:update-log="updateLog" />
    </div>
  </div>
</template>

<script>
import modal from "./modal/Modal.vue";
import CategoryItem from "./CategoryItem.vue";
import { APIService } from "../BackendApiService.js";

export default {
  name: "Categories",
  components: {
    CategoryItem,
    modal
  },
  props: ["categories"],
  methods: {
    showAddCatModal() {
      this.isAddCatModalVisible = true;
    },
    closeAddCatModal() {
      this.isAddCatModalVisible = false;
    },
    SubmitAddCatModal(e) {
      e.preventDefault();
      let api_serv = new APIService();
      const cat = {
        name: this.name,
        user: localStorage.user_id
      };
      api_serv
        .createCategory(cat)
        .then(res => {
          if (res.data.code == "010") {
            this.$emit("update-category");
            this.name = "";
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isAddCatModalVisible = false;
    },
    updateLog() {
      this.$emit("update-log");
    }
    // other JS methods here
  },
  data() {
    return {
      isAddCatModalVisible: false,
      name: ""
    };
  }
};
</script>

<style scoped>
.btn {
  border-color: rgb(21, 156, 235);
  color: rgb(21, 156, 235);
  margin: 5px;
}
.btn:hover {
  background-color: rgb(21, 156, 235);
  color: white;
}
</style>
