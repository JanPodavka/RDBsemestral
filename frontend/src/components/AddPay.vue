<template>
  <v-container>
    <v-select
      v-model="selectedItem"
      label="Select"
      :items="['Platební karta', 'Převod', 'Hotovost']"
    ></v-select>

    <v-row v-if="selectedItem === 'Platební karta'">
      <v-col cols="12" sm="4">
        <v-text-field v-model="cardNumber" label="Číslo karty"></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model="expiryDate" label="Expiry Date"></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model="cvv" label="CVV"></v-text-field>
      </v-col>
    </v-row>

    <v-row v-else-if="selectedItem === 'Převod'">
      <v-col cols="12" sm="6">
        <v-text-field v-model="bankName" label="Bank Name"></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field v-model="accountNumber" label="Account Number"></v-text-field>
      </v-col>
    </v-row>

    <v-row v-else-if="selectedItem === 'Hotovost'">
      <v-col cols="12" sm="6">
        <v-text-field v-model="cashAmount" label="Cash Amount"></v-text-field>
      </v-col>
    </v-row>

    <v-btn v-if="selectedItem === 'Platební karta'" color="primary" @click="payCard">Zaplatit</v-btn>
    <v-btn v-if="selectedItem === 'Převod'" color="primary" @click="payTrans">Zaplatit</v-btn>
    <v-btn v-if="selectedItem === 'Hotovost'" color="primary" @click="payMoney">Zaplatit</v-btn>
  </v-container>
</template>

<script>
import axios from "axios";
import { ref } from 'vue';

const dataPlatba = ref([]);
const dataTest = ref([]);

export default {
  name: "AddPay",
  data() {
    return {
      selectedItem: null,
      cardNumber: "",
      expiryDate: "",
      cvv: "",
      bankName: "",
      accountNumber: "",
      cashAmount: ""
    };
  },
  methods: {
   payCard() {
    // Clear all text fields

    dataPlatba.value = {"typ":"Karta","spz":"QQQ4567","data":{"cislo_karty":this.cardNumber,"platnost":"1715002361","vlastnik":this.cvv,"castka":20,"datum_platby":"1715002361"}};  // Assuming response.data is an array of objects
    axios.post(`http://127.0.0.1:5000/api/karta`,{
      platba:dataPlatba.value
     })
      .then(response => {

      })
      .catch(error => {
        console.error('Error fetching data from Flask backend:', error);
      });
     this.cardNumber = "";
    this.expiryDate = "";
    this.cvv = "";
    this.bankName = "";
    this.accountNumber = "";
    this.cashAmount = "";
  },
    payTrans() {
      // Clear all text fields
      this.cardNumber = "";
      this.expiryDate = "";
      this.cvv = "";
      this.bankName = "";
      this.accountNumber = "";
      this.cashAmount = "";

      // Call your function here
      // For now, it's left blank
    },
    payMoney() {
      // Clear all text fields
      this.cardNumber = "";
      this.expiryDate = "";
      this.cvv = "";
      this.bankName = "";
      this.accountNumber = "";
      this.cashAmount = "";

      // Call your function here
      // For now, it's left blank
    }
  }
};
</script>

<style scoped>

</style>
