<template>
  <v-container>
    <v-select
      v-model="selectedItem"
      label="Možnosti platby"
      :items="['Platební karta', 'Převod', 'Hotovost']"
    ></v-select>

    <v-row v-if="selectedItem === 'Platební karta'">
      <v-col cols="12" sm="6">
        <v-text-field v-model="spz" label="SPZ"></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model="cardNumber" label="Číslo karty"></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model="expiryDate" label="Platnost karty"></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model="owner" label="Vlastník"></v-text-field>
      </v-col>
      <v-col cols="12" sm="4">
        <v-text-field v-model="cardMoney" label="Částka"></v-text-field>
      </v-col>
    </v-row>

    <v-row v-else-if="selectedItem === 'Převod'">
      <v-col cols="12" sm="6">
        <v-text-field v-model="spz" label="SPZ"></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field v-model="bankNumber" label="Číslo účtu"></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field v-model="bankCode" label="Kód banky"></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field v-model="cashAmount" label="Částka"></v-text-field>
      </v-col>
    </v-row>

    <v-row v-else-if="selectedItem === 'Hotovost'">
      <v-col cols="12" sm="6">
        <v-text-field v-model="spz" label="SPZ"></v-text-field>
      </v-col>
      <v-col cols="12" sm="6">
        <v-text-field v-model="cashAmount" label="Částka"></v-text-field>
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
      bankNumber: "",
      owner: "",
      bankCode: "",
      accountNumber: "",
      spz: "",
      cashAmount: ""
    };
  },
  methods: {
   payCard() {
    // Clear all text fields
    dataPlatba.value = {"typ":"Karta","spz":this.spz,"data":{"cislo_karty":this.cardNumber,"platnost":this.expiryDate,"vlastnik":this.owner,"castka":this.cardMoney}};  // Assuming response.data is an array of objects
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
    this.owner = "";
    this.bankCode = "";
    this.accountNumber = "";
    this.cashAmount = "";
    this.cardMoney = "";
    this.spz = ""
  },
    payTrans() {
    dataPlatba.value = {"typ":"Prevod","spz":this.spz,"data":{"cislo_uctu":this.bankNumber,"kod_banky":this.bankCode,"castka":this.cashAmount}};  // Assuming response.data is an array of objects
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
    this.owner = "";
    this.bankCode = "";
    this.accountNumber = "";
    this.cashAmount = "";
    this.cardMoney = "";
      this.spz = ""
    },
    payMoney() {
    dataPlatba.value = {"typ":"Hotovost","spz":this.spz,"data":{"castka":this.cashAmount}};  // Assuming response.data is an array of objects
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
    this.owner = "";
    this.bankCode = "";
    this.accountNumber = "";
    this.cashAmount = "";
    this.cardMoney = "";
    this.spz = ""
    }
  }
};
</script>

<style scoped>

</style>
