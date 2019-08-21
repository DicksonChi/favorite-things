<template>
  <div id="app">
    <Header />

    <!-- for the categories-->
    <div class="row block">
      <div class="col-lg-6 col-sm-12">
        <h3 align="center">Categories</h3>
        <Categories
          v-bind:categories="categories"
          v-on:update-log="updateLog"
          v-on:update-category="updateCategory"
        />
      </div>

      <!-- for the logs-->
      <div class="col-lg-6 col-sm-12">
        <h3 align="center">Logs</h3>
        <Logs v-bind:logs="logs" />
      </div>
    </div>
  </div>
</template>

<script>
import Categories from "../components/Category";
import Header from "../components/Header";
import Logs from "../components/Logs";
import { APIService } from "../BackendApiService.js";
export default {
  name: "app",
  components: {
    Header,
    Categories,
    Logs
  },
  data() {
    return {
      categories: [],
      logs: [],
      user_id: null
    };
  },
  created() {
    this.user_id = localStorage.user_id;
    let api_serv = new APIService();
    api_serv
      .getCategory(this.user_id)
      .then(res => {
        if (res.data.code == "010") {
          this.categories = res.data.categories;
        }
      })
      .catch(err => {
        console.log(err);
      });

    api_serv
      .getLogs(this.user_id)
      .then(res => {
        if (res.data.code == "010") {
          this.logs = res.data.logs;
        }
      })
      .catch(err => {
        console.log(err);
      });
  },
  methods: {
    updateLog() {
      let api_serv = new APIService();
      api_serv
        .getLogs(this.user_id)
        .then(res => {
          if (res.data.code == "010") {
            this.logs = res.data.logs;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    updateCategory() {
      let api_serv = new APIService();
      api_serv
        .getCategory(this.user_id)
        .then(res => {
          if (res.data.code == "010") {
            this.categories = res.data.categories;
            this.updateLog();
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, Helvetica, sans-serif;
  line-height: 1.4;
}
.block {
  margin: 5px;
}
</style>
