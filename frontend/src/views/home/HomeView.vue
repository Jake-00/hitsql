<script setup lang="ts">
  import CodeEditor from '../../components/CodeEditor.vue'
</script>

<template>
  <div class="layout-demo">
    <a-layout>
      <a-layout-header>HitSQL</a-layout-header>
      <a-layout>
        <CodeEditor/>
      </a-layout>
      <a-layout-footer>Footer</a-layout-footer>
    </a-layout>
  </div>
</template>
<style scoped>
.layout-demo :deep(.arco-layout-header),
.layout-demo :deep(.arco-layout-footer) {
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: var(--color-white);
  font-size: 16px;
  font-stretch: condensed;
  /* text-align: center; */
}


.layout-demo :deep(.arco-layout-header),
.layout-demo :deep(.arco-layout-footer) {
  height: 10vh;
  background-color: var(--color-primary-light-4);
}

.layout-demo :deep(.arco-layout-sider) {
  width: 50vw;
  background-color: var(--color-primary-light-3);
  min-width: 50vw;
  max-width: 70vw;
  height: 80vh;
}

.layout-demo :deep(.arco-layout-content) {
  /* background-color: rgb(var(---6)); */
  background-color: #f6f6f6;
}
</style>