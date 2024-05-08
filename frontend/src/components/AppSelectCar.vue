<template>
  <v-navigation-drawer app>
    <!-- List of blank data here -->
    <v-list-item :style="{ 'font-weight': 'bold', 'font-size': '20px' }">Výběr SPZ automobilu</v-list-item>
    <v-divider></v-divider>
    <v-list>
      <v-list-item-group>
        <v-list-item v-for="(item, index) in dataspz" :key="index" @click="handleItemClick(item)">
          <v-list-item-content>
            <v-list-item-title>{{ item }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
import { ref } from 'vue';
import axios from "axios";

const dataspz = ref([]);


axios.get('http://127.0.0.1:5000/api/dataSPZ')
  .then(response => {
    console.log(response.value)
    dataspz.value = response.data;  // Assuming response.data is an array of objects
  })
  .catch(error => {
    console.error('Error fetching data from Flask backend:', error);
  });


</script>



