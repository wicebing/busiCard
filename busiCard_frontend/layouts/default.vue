<script setup>
import { NLayoutFooter, NLayoutHeader,  } from 'naive-ui'
// import { useUserStore } from '../composables/user.js'
const useStore = useUserStore()
</script>

<template>
    <div>
        <div>
          <slot name="main"/>
        </div>

        <n-layout-footer class="p-6 flex flex-wrap item-center justify-between font-mono">
            <p class="text-white font-bold ">Copyright (c) 2023 yAbI Lab</p>
            <NuxtLink to="/"><p class="text-white font-bold hover:bg-sky-500">Personal Business Card</p></NuxtLink>
            
            <slot name="footer"/>

        </n-layout-footer>
    </div>
  </template>
  
  <style scoped>
  .n-layout-header {
    background: rgba(0, 104, 189, 0.2);
    padding: 24px;
  }
  .n-layout-footer {
    background: rgba(0, 42, 75, 0.719);
    padding: 24px;
  }

  </style>