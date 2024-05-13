<template>
  <v-footer height="40" app>
    <span class="mx-auto">&copy; {{ new Date().getFullYear() }} Autoři: Jan Podávka, Ondřej Soukup</span>
    <span class="text-left">RDB semestrální práce</span>
  </v-footer>
</template>

<script setup>

</script>

<style scoped lang="sass">
  .social-link :deep(.v-icon)
    color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity))
    text-decoration: none
    transition: .2s ease-in-out

    &:hover
      color: rgba(25, 118, 210, 1)
</style>
