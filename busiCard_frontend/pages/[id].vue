<script setup>
import { apiConfig } from "@/apiConfig";

const route = useRoute()
const { id } = route.params

const backgroundColor = ref('#0068bd33');
const personalLink = reactive({})
const personalAllLink = reactive({})
const personalProfile = reactive({})

async function getPerson () {
  console.log('getPerson')
  try{
      const { data, pending, refresh, error } = await useFetch(`/api/businessCard/?auth=${id}`, {
          method: 'GET',
          baseURL:apiConfig.API_ENDPOINT,
      })

      if (data.value) {
          Object.assign(personalProfile, data.value.results[0])
          console.log('personalProfile',personalProfile)
          backgroundColor.value = personalProfile.color
          getLinks (personalProfile)
      } else {
          console.log('error',error)
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
          console.log('error',error)
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
{{personalProfile}}
{{ personalAllLink }}

<div class="py-10 px-6" :style="{ background: backgroundColor }">
    <div class="space-y-4">

    </div>
</div>
</template>

