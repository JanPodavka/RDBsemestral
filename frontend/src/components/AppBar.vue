<template>
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
    </v-tabs>
    <v-spacer></v-spacer>
  </v-app-bar>



</template>

<script setup>
import { ref } from 'vue';

const tab = ref(1); // Default tab

</script>

