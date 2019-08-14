<template>
  <div class="log-item row">
    <div class="col-12">
      <div>
        <h5>{{ log.extra_details }}</h5>
      </div>
      <br />

      <div class="log-time action">
        <h6><i class="fa fa-clock-o"></i> {{ log.log_time | moment }}</h6>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment";
export default {
  name: "LogItem",
  props: ["log"],
  filters: {
    moment: function(date) {
      return moment(date).format("MMMM Do YYYY, h:mm a");
    }
  },
  methods: {
    // other JS methods here
  }
};
</script>

<style scoped>
.log-item {
  background: white;
  padding: 20px;
  color: rgb(21, 156, 235);
  border-bottom: 1px #ccc dotted;
}
.log-time {
  color: rgb(31, 90, 126);
}
</style>
