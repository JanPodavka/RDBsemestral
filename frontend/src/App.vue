<template>

  <v-app>
    <v-app-bar app>
    <v-spacer></v-spacer>
      <v-tabs
      v-model="tab"
      align-tabs="center"
      color="deep-purple-accent-4"
    >
      <v-tab :value="1">Přehled průjezdů</v-tab>
      <v-tab :value="2">Přehled plateb</v-tab>
      <v-tab :value="3">Přidat platbu</v-tab>
        <v-tab :value="4">Generování dat</v-tab>
    </v-tabs>
    <v-spacer></v-spacer>
  </v-app-bar>
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
    <v-main>
      <template v-if="tab === 1">
        <HelloWorld  :tableDataFromBackend="tabledata"/>
      </template>
      <template v-else-if="tab === 2">
        <div>
          <AppPay  :tableDataFromBackend="payData"/>
        </div>
      </template>
      <template v-else-if="tab === 3">
        <div>
          <AddPay :tableDataFromBackend="spz_now" />
        </div>
      </template>
      <template v-else-if="tab === 4">
        <div>
          <ImportDat/>
        </div>
      </template>
    </v-main>
    <AppFooter />
  </v-app>
</template>

<script setup>
import { ref } from 'vue';

import axios from "axios";
import ImportDat from "@/components/ImportDat";
const tab = ref(1); // Default tab
const dataspz = ref([]);
let tabledata = ref([]);
let payData = ref([]);
let spz_now = ref("QQQ4567");


axios.get('http://127.0.0.1:5000/api/dataSPZ')
  .then(response => {
    console.log(response.value)
    dataspz.value = response.data;  // Assuming response.data is an array of objects
  })
  .catch(error => {
    console.error('Error fetching data from Flask backend:', error);
  });



const handleItemClick = (item) => {
  spz_now = item
  console.log(`Clicked item: ${item}`);

  axios.get(`http://127.0.0.1:5000/api/dataPrujezd?spz=${item}`)
    .then(response => {
      tabledata = response.data;
      console.log('Table data:', tabledata);
    })
    .catch(error => {
      console.error('Error fetching table data:', error);
    });
  /// Add pay function in table
  axios.get(`http://127.0.0.1:5000/api/dataPlatba?spz=${item}`)
    .then(response => {
      payData = response.data;
      console.log('Table data:', tabledata);
    })
    .catch(error => {
      console.error('Error fetching table data:', error);
    });



};
</script>
