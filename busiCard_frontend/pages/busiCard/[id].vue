<script setup>
import { NButton, NTabs, NTabPane, NSwitch, NDrawer, NDrawerContent, NSelect } from 'naive-ui'
import { NFormItemRow, NInput, NForm, NDatePicker } from 'naive-ui'
import { apiConfig } from "@/apiConfig";

const useStore = useUserStore()
const route = useRoute()
console.log('test',route.params.id)

const errors = ref([])
const personalLink = reactive({})
const personalAllLink = reactive({})
const personalProfile = reactive({})
const editing = reactive([])
const activeDrawerLinkEdit = ref(false)
const activeDrawerLinkAdd = ref(false)
const placementDrawer = ref('right')

const backgroundColor = ref('#0068bd33');

function resetColor () {
  backgroundColor.value = '#0068bd33';
}



function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function truncateUrl(url, length = 30) {
    return url.length > length ? url.substring(0, length) + "..." : url;
}

async function getPerson () {
  console.log('getPerson')
  try{
      const { data, pending, refresh, error } = await useFetch(`/api/businessCard/?user=${useStore.id}`, {
          method: 'GET',
          baseURL:apiConfig.API_ENDPOINT,
          headers: {
              Authorization: `JWT ${useStore.token}` 
          }
      })

      if (data.value) {
          Object.assign(personalProfile, data.value.results[0])
          console.log('personalProfile',personalProfile)
          backgroundColor.value = personalProfile.color
      } else {
          console.log('error',error)
      }
  } catch (err) {
      console.log('err',err)
  }
}

async function getLinks () {
  console.log('getLinks')
  for (const key in personalLink) {
        delete personalLink[key];
  }
  for (const key in personalAllLink) {
      delete personalAllLink[key];
  }
  try{
      const { data, pending, refresh, error } = await useFetch(`/api/personalLink/?user=${useStore.id}`, {
          method: 'GET',
          baseURL:apiConfig.API_ENDPOINT,
          headers: {
              Authorization: `JWT ${useStore.token}` 
          }
      })

      if (data.value) {
        
          // Get today's date
          const today = new Date();
          today.setHours(0, 0, 0, 0);  // Set the time to 00:00:00

          // Filter personalLink where endDate is not before today
          const filteredPersonalLink = data.value.results.filter(link => {
              const endDate = new Date(link.endDate);
              return endDate >= today;
          });
          Object.assign(personalLink, filteredPersonalLink)
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
    getLinks()
})

</script>

<template>
  <div class="py-10 px-6" :style="{ background: backgroundColor }">
    <div class="space-y-4">
        test
        {{ useStore }}
        {{ personalProfile }}
        {{ personalLink }}
    </div>
  </div>

</template>

<style scoped>
.defalutBackground {
  background: rgba(0, 104, 189, 0.2);
  padding: 24px;
}
</style>