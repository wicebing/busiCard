<script setup>
import { apiConfig } from "@/apiConfig";
import { NDivider } from 'naive-ui'

const route = useRoute()

const { id } = route.params

const backgroundColor = ref('#0068bd33');
const personalLink = reactive({})
const personalAllLink = reactive({})
const personalProfile = reactive({})

async function getPerson () {
  console.log('getPerson',`/api/businessCard/?auth=${id}`)
  try{
      const data  = await $fetch(`/api/businessCard/?auth=${id}`, {
          method: 'GET',
          baseURL:apiConfig.API_ENDPOINT,
      })
    //   console.log('datagetPerson',data)
      if (data) {
        // console.log('personalProfile', data.results[0])
        Object.assign(personalProfile, data.results[0])
        console.log('personalProfile',personalProfile)
        backgroundColor.value = personalProfile.color
        getLinks (personalProfile)
      } else {
        console.log('errorgetPerson')
      }
  } catch (err) {
      console.log('err',err)
  }
}

async function getLinks (personalProfile) {
  console.log('getLinks')
  for (const key in personalAllLink) {
      delete personalAllLink[key];
  }
  try{
      const { data, pending, refresh, error } = await useFetch(`/api/personalLink/?user=${personalProfile.user}&active=1`, {
          method: 'GET',
          baseURL:apiConfig.API_ENDPOINT,
      })

      if (data.value) {
          Object.assign(personalAllLink, data.value.results)
          console.log('personalLink',personalLink)
      } else {
          console.log('errorgetLinks',error)
          errors.value.push(error.value.data)
      }
  } catch (err) {
      console.log('err',err)
  }
}

onMounted(() => {
  getPerson()
})

</script>

<template>
匹配到的 Id: <span class="text-5xl font-semibold text-blue-600">{{ id }}</span>

<div class="py-10 px-6" :style="{ background: backgroundColor }">
    <div class="space-y-4">
        {{personalProfile}}
        <n-divider />
        {{ personalAllLink }}
    </div>
</div>
</template>

