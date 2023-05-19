<script setup>
import { apiConfig } from "@/apiConfig";
const route = useRoute()
const { id } = route.params

const useStore = useUserStore()
const errors = ref([])

function toBusiCard() {
  navigateTo(`/${id}`)
}

async function getCurrentUser() {
    errors.value = []
    console.log('getCurrentUser by token',useStore.token)
    try{
        const { data, pending, refresh, error } = await useFetch('/api/whoami/', {
            method: 'GET',
            baseURL: apiConfig.API_ENDPOINT,
            headers: {
                Authorization: `JWT ${useStore.token}`,
            },
        });

        if (error.value) {
            console.log('Error:', error.value);
        } else {
            console.log('Current user:', data.value);
            if (data.value) {
                useStore.setUserDetail(data.value.id,
                data.value.username,
                data.value.email,
                data.value.is_staff,
                data.value.is_superuser,
                ) 
            } 
            console.log('getUser',useStore.getUserDetail())
            navigateTo('/')
        }       
    } catch (error) {
        console.log('ALLerror',error)
        errors.value.push('please try again')
    }
}

onMounted(() => {
  if (!id){
    useStore.initStore()
    if (useStore.isAuthenticated) {
      getCurrentUser()
    }    
  } else {
    // useStore.initStore()
    // toBusiCard()
  }
})
</script>


<template>
  <NuxtLayout name="default">
    <template #header> 
    </template>
    <template #main> 
      <NuxtPage/>
    </template>
    <template #footer> 
      <footerLogin/>
    </template>
  </NuxtLayout>
</template>

<style scoped>

</style>