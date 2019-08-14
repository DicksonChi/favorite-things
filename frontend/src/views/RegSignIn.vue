<template>
  <div id="app">
    <div class="login">
      <p>
        Please enter a user ID (email) to use this application or to continue
        from your last session.
      </p>
      <br />
      <form @submit="Signin">
        <div class="form-group">
          <input
            type="email"
            placeholder="email address"
            class="form-control"
            id="username"
            v-model="username"
          />
        </div>
        <br />
        <div class="form-group">
          <button type="submit" class="btn btn-primary">
            Contine
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { APIService } from "../BackendApiService.js";
export default {
  name: "RegSignIn",
  components: {},
  data() {
    return {
      username: "",
      user_id: ""
    };
  },
  methods: {
    Signin(e) {
      e.preventDefault();
      // validate that it is an email that is entered
      let emailReg = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
      if (this.username == "" || !emailReg.test(this.username)) {
        alert(
          "Please Enter a valid username and make sure it is an email input"
        );
      } else {
        let api_serv = new APIService();
        // console.log(new APIService());
        api_serv
          .getUser(this.username)
          .then(res => {
            if (res.data.code == "010") {
              this.user_id = res.data.id;
              localStorage.user_id = res.data.id;
              this.$router.replace({ name: "home" });
            }
          })
          .catch(err => {
            console.log(err);
            let create_use = new APIService();
            create_use
              .createUser(this.username)
              .then(res => {
                if (res.data.code == "010") {
                  this.user_id = res.data.id;
                  localStorage.user_id = res.data.id;
                  this.$router.replace({ name: "home" });
                }
              })
              .catch(err => console.log(err));
          });
        //this.$router.replace({ name: "home" });
      }
    }

    // other JS methods here
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: Arial, Helvetica, sans-serif;
  background-color: black;
  line-height: 1.4;
}
.login {
  width: 500px;
  border: 1px solid #cccccc;
  background-color: rgb(247, 241, 241);
  margin: auto;
  margin-top: 200px;
  padding: 20px;
}
.btn {
  width: 100px;
  background: rgb(21, 156, 235);
}
.btn:hover {
  color: rgb(21, 156, 235);
  background: #ffffff;
}
</style>
