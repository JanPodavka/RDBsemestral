<template>
  <v-container class="fill-height">
    <v-responsive
      class="align-centerfill-height mx-auto"
      max-width="900"
    >
      <div>
        <v-data-table
          :headers="headers"
          :items="localTableData"
          :items-per-page="5"
          class="elevation-1"
        ></v-data-table>
      </div>
      <div class="py-4" />

      <!-- Move the h2 elements here -->

    </v-responsive>
  </v-container>
</template>

<script setup>
import {ref, onMounted, defineProps, watch} from 'vue';
import axios from "axios";
const props = defineProps({
  tableDataFromBackend: Array
});
const km = ref([]);
const penize = ref([]);

const localTableData = ref(props.tableDataFromBackend);

console.log(props)
watch(
  () => props.tableDataFromBackend,
  (newVal) => {
    console.log('Prop value changed:', newVal);
    localTableData.value = newVal;




  },
  { immediate: true } // Update immediately when the component is mounted
);
</script>
