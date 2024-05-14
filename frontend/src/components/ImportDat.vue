<template>
  <v-container>
    <v-row>
      <v-col cols="12" sm="6">
        <v-text-field
          v-model="numberOfRecords"
          label="Počet záznamů"
          outlined
        ></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-btn color="primary" @click="generateRecords">Vygenerovat</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "ImportDat",
  data() {
    return {
      numberOfRecords: "" // To store the value of the text field
    };
  },
  methods: {
    generateRecords() {
      console.log('Error fetching data from Flask backend:', this.numberOfRecords);
      axios.post(`http://127.0.0.1:5000/api/generate`,{
      num:this.numberOfRecords
     })
      .then(response => {

      })
      .catch(error => {
        console.error('Error fetching data from Flask backend:', error);
      });

      this.numberOfRecords = ""
    }
  }
};
</script>

<style scoped>

</style>
