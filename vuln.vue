<template>
  <div v-html="getData(maliciousData)"></div>
</template>
<script setup>
const maliciousData = "<img src=x onerror=alert(1)//>";
function getData(data) {
  return data;
}
</script>
