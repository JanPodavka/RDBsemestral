<template>
  <v-container class="fill-height">
    <v-responsive
      class="align-centerfill-height mx-auto"
      max-width="900"
    >
      <v-img
        class="mb-4"
        height="150"
        src="@/assets/logo.png"
      />
       <div>
        <h2>Data2 from Flask Backend:</h2>
        <p>{{ dataFromBackend }}</p>
      </div>
      <div>
        <h2>Data from Flask Backend in Table:</h2>
        <v-data-table
          :headers="headers"
          :items="dataFromBackend"
          :items-per-page="5"
          class="elevation-1"
        ></v-data-table>
      </div>
      <div class="text-center">
        <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

        <h1 class="text-h2 font-weight-bold">Vuetify</h1>
      </div>

      <div class="py-4" />


    </v-responsive>
  </v-container>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';

const dataFromBackend = ref([]);

axios.get('http://127.0.0.1:5000/api/data')
  .then(response => {
    dataFromBackend.value = response.data;  // Assuming response.data is an array of objects
  })
  .catch(error => {
    console.error('Error fetching data from Flask backend:', error);
  });

</script>
