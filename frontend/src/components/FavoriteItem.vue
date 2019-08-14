<template>
  <div class="favorite-item row">
    <modal v-if="isEditModalVisible || isViewModalVisible">
      <h3 slot="header" class="modal-title">
        <span v-if="isEditModalVisible">Edit This Item</span>
        <span v-if="isViewModalVisible">View This Item</span>
      </h3>

      <div slot="body">
        <p>
          Date Modified:
          <span style="color: black">{{
            favorite.date_modified | moment
          }}</span>
        </p>
        <form @submit="SubmitcloseEditModal">
          <div class="form-group">
            <label for="rank">Rank</label>
            <input
              type="number"
              class="form-control"
              id="rank"
              v-model="favorite.ranking"
              v-bind:readonly="isViewModalVisible"
            />
          </div>
          <div class="form-group">
            <label for="title"
              >Title <span v-if="isEditModalVisible">*</span></label
            >
            <input
              type="text"
              class="form-control"
              v-model="favorite.title"
              id="title"
              maxlength="20"
              required
              v-bind:readonly="isViewModalVisible"
            />
          </div>
          <div class="form-group">
            <label for="title">Description</label>
            <textarea
              type=""
              class="form-control"
              id="description"
              v-model="favorite.description"
              v-bind:readonly="isViewModalVisible"
            >
            </textarea>
          </div>
          <label
            title="Please you are required to enter the value with keys attached"
            >Metadata</label
          ><br />
          <div class="form-group ">
            <div
              class="row"
              v-bind:key="index"
              v-for="(item, index) in favorite.metadata"
            >
              <div class="col-3">
                <input
                  type="text"
                  placeholder="key"
                  class="form-control"
                  v-model="item.key"
                  v-bind:readonly="isViewModalVisible"
                />
              </div>
              <div class="col-9">
                <input
                  type="text"
                  placeholder="value"
                  class="form-control"
                  id="description"
                  v-model="item.value"
                  v-bind:readonly="isViewModalVisible"
                />
              </div>
            </div>
            <div class="row">
              <div class="col-7"></div>
              <div class="col-5 action" v-if="!isViewModalVisible">
                <button class="btn btn-sm" type="button" @click="AddMetadata">
                  <i class="fa fa-plus"> Add more</i>
                </button>
              </div>
            </div>
          </div>
          <div class="form-group">
            <button
              type="submit"
              class="btn btn-outline-info"
              v-if="!isViewModalVisible"
            >
              Update
            </button>
            <button
              type="button"
              class="btn btn-outline-info"
              @click="closeModal()"
            >
              Close
            </button>
          </div>
        </form>
      </div>
    </modal>
    <div class="col-1">
      {{ favorite.ranking }}
    </div>
    <div class="col-3">
      {{ favorite.title }}
    </div>
    <div class="col-4">
      {{ favorite.date_added | moment }}
    </div>
    <div class="col-4 action">
      <button
        class="btn btn-sm"
        title="view other information associated to this thing"
        @click="showViewModal"
      >
        <i class="fa fa-eye"></i>
      </button>
      <button class="btn btn-sm" title="edit this thing" @click="showEditModal">
        <i class="fa fa-edit"></i>
      </button>
      <button class="btn btn-sm" title="trash this thing" @click="destroyThing">
        <i class="fa fa-trash"></i>
      </button>
    </div>
  </div>
</template>

<script>
import modal from "./modal/Modal.vue";
import { APIService } from "../BackendApiService.js";
import moment from "moment";
export default {
  name: "FavoriteItem",
  props: ["favorite"],
  components: {
    modal
  },
  filters: {
    moment: function(date) {
      return moment(date).format("MMMM Do YYYY, h:mm:ss a");
    }
  },
  data() {
    return {
      isViewModalVisible: false,
      isEditModalVisible: false
    };
  },
  methods: {
    AddMetadata() {
      this.favorite.metadata.push({ key: "", value: "" });
    },
    showViewModal() {
      this.isViewModalVisible = true;
      this.isEditModalVisible = false;
    },

    closeModal() {
      this.isViewModalVisible = false;
      this.isEditModalVisible = false;
    },
    showEditModal() {
      this.isViewModalVisible = false;
      this.isEditModalVisible = true;
    },
    SubmitcloseEditModal(e) {
      e.preventDefault();
      if (
        this.favorite.description != "" &&
        this.favorite.description.length < 10
      ) {
        alert(
          "Item Description length must be at least 10 characters or left empty."
        );
        return;
      }
      let api_serv = new APIService();
      this.favorite.metadata = api_serv.prepareMeta(this.favorite.metadata);
      api_serv
        .updateThing(this.favorite)
        .then(res => {
          if (res.data.code == "010") {
            this.$emit("update-favorite");
          }
        })
        .catch(err => {
          console.log(err);
        });
      this.isEditModalVisible = false;
    },

    destroyThing(e) {
      e.preventDefault();
      let api_serv = new APIService();
      api_serv
        .deleteThing(this.favorite)
        .then(res => {
          if (res.status == 204) {
            this.$emit("update-favorite");
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
    // other JS methods here
  }
};
</script>

<style scoped>
.favorite-item {
  background: rgb(247, 241, 241);
  padding: 10px;
  color: rgb(36, 37, 37);
  border-bottom: 1px #ccc dotted;
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
