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
      this.cardNumber = "";
      this.expiryDate = "";
      this.cvv = "";
      this.bankName = "";
      this.accountNumber = "";
      this.cashAmount = "";

      // Call your function here
      // For now, it's left blank
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
