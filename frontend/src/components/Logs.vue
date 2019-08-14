<template>
  <div>
    <div v-bind:key="log.id" v-for="log in logs">
      <LogItem v-bind:log="log" />
    </div>
  </div>
</template>

<script>
import LogItem from "./LogItem.vue";
export default {
  name: "Logs",
  components: {
    LogItem
  },
  props: ["logs"]
};
</script>

<style scoped></style>
