<script setup>
import { NLayoutHeader,  } from 'naive-ui'
const useStore = useUserStore()
</script>

<template>
  <n-layout-header>
    <nav class="flex items-center justify-between flex-wrap font-mono">
      <NuxtLink to="/" >
          <span class="box-decoration-clone bg-gradient-to-r from-indigo-600 to-pink-500 text-white px-2 font-bold font-mono text-xl">
            BusiCard
          </span>
      </NuxtLink>
      <div v-if=useStore.isAuthenticated>
        <span> Hello, {{ useStore.username }} </span>             
      </div>
      <headerNav/>
    </nav>
  </n-layout-header>
</template>
<style scoped>
.n-layout-header {
  background: rgba(0, 104, 189, 0.2);
  padding: 24px;
}
</style>