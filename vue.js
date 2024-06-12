<template>
            <div
              v-html="
                convertNewlinesToHtml(
                  extensionsStore.currentExtension.description
                )
              "
            ></div>
</template>
<script setup>
import { useExtensionsStore } from "stores/extensions";
const extensionsStore = useExtensionsStore();
function convertNewlinesToHtml(data) {
  if (!data) {
    return "";
  }
  return data.replace(/\r?\\n|\r/g, "<br />");
}
</script>
