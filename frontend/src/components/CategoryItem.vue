<template>
  <div class="category-item row">
    <modal v-if="isAddModalVisible">
      <h3 slot="header" class="modal-title">
        Add a Thing to the List
      </h3>

      <div slot="body">
        <form @submit="AddThingModal">
          <div class="form-group">
            <label for="rank">Rank</label>
            <input
              type="number"
              class="form-control"
              id="rank"
              v-model="ranking"
            />
          </div>
          <div class="form-group">
            <label for="title">Title*</label>
            <input
              type="text"
              class="form-control"
              id="title"
              required
              v-model="title"
              maxlength="20"
            />
          </div>
          <div class="form-group">
            <label for="title">Description</label>
            <textarea
              type="text"
              class="form-control"
              id="description"
              v-model="description"
            >
            </textarea>
          </div>
          <div>
            <label
              title="Please you are required to enter the value with keys attached"
              >Metadata</label
            ><br />
            <div class="form-group ">
              <div
                class="row"
                v-bind:key="index"
                v-for="(item, index) in metadata"
              >
                <div class="col-3">
                  <input
                    type="text"
                    placeholder="key"
                    class="form-control"
                    v-model="item.key"
                  />
                </div>
                <div class="col-9">
                  <input
                    type="text"
                    placeholder="value"
                    class="form-control"
                    v-model="item.value"
                  />
                </div>
              </div>

              <div class="row">
                <div class="col-7"></div>
                <div class="col-5 action">
                  <button class="btn btn-sm" type="button" @click="AddMetadata">
                    <i class="fa fa-plus"></i> create more
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="form-group row">
            <button type="submit" class="btn btn-outline-info">Submit</button>
            <button
              type="button"
              class="btn btn-outline-info"
              @click="closeAddModal"
            >
              close
            </button>
          </div>
        </form>
      </div>
    </modal>
    <div class="col-7">
      <br />
      <b>{{ category.name }}</b>
    </div>
    <div class="col-5 action">
      <button
        class="btn"
        title="view things in this category"
        @click="viewList = !viewList"
      >
        <i class="fa fa-bars"> </i>
      </button>
      <button
        class="btn"
        title="add a new thing to this category"
        @click="showAddModal"
      >
        <i class="fa fa-plus"></i>
      </button>
    </div>

    <div class="col-12" v-if="viewList">
      <Favorites
        v-bind:favorites="favorites"
        v-on:update-favorite="updateFavorite"
      />
    </div>
  </div>
</template>

<script>
import modal from "./modal/Modal.vue";
import Favorites from "./Favorite.vue";
import { APIService } from "../BackendApiService.js";
export default {
  name: "CategoryItem",
  props: ["category"],
  components: {
    Favorites,
    modal
  },
  data() {
    return {
      isAddModalVisible: false,
      favorites: [],
      viewList: true,
      ranking: "",
      title: "",
      description: "",
      metadata: [{ key: "", value: "" }]
    };
  },
  methods: {
    AddMetadata() {
      this.metadata.push({ key: "", value: "" });
    },
    showAddModal() {
      this.isAddModalVisible = true;
    },
    closeAddModal() {
      this.isAddModalVisible = false;
      this.metadata = [{ key: "", value: "" }];
    },
    updateFavorite() {
      let api_serv = new APIService();
      api_serv
        .getFavThings(this.category.id, localStorage.user_id)
        .then(res => {
          if (res.data.code == "010") {
            this.favorites = res.data.favThings;
            this.metadata = [{ key: "", value: "" }];
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.$emit("update-log");
    },
    AddThingModal(e) {
      e.preventDefault();
      if (this.description != "" && this.description.length < 10) {
        alert("Text length must be at least 10 characters or left empty.");
        return;
      }
      let api_serv = new APIService();
      // prepare the string to be passed to the backend
      const met_data = api_serv.prepareMeta(this.metadata);
      const newThing = {
        ranking: this.ranking,
        title: this.title,
        description: this.description,
        category: this.category.id,
        user: localStorage.user_id,
        metadata: met_data
      };
      api_serv
        .createThing(newThing)
        .then(res => {
          if (res.data.code == "010") {
            api_serv
              .getFavThings(this.category.id, localStorage.user_id)
              .then(res => {
                if (res.data.code == "010") {
                  this.favorites = res.data.favThings;
                  this.metadata = [{ key: "", value: "" }];
                  this.ranking = "";
                  this.title = "";
                  this.description = "";
                  //send an emit function to logs
                  this.$emit("update-log");
                }
              })
              .catch(err => {
                console.log(err);
              });
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isAddModalVisible = false;
    }
    // other JS methods hered
  },

  created() {
    let api_serv = new APIService();
    api_serv
      .getFavThings(this.category.id, localStorage.user_id)
      .then(res => {
        if (res.data.code == "010") {
          this.favorites = res.data.favThings;
        }
      })
      .catch(err => {
        console.log(err);
      });
  }
};
</script>

<style scoped>
.category-item {
  background: #ffffff;
  padding: 10px;
  padding-left: 20px;
  border: 1px rgb(21, 156, 235);
}
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
