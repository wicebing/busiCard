<script setup>
import { NButton, NTabs, NTabPane, NSwitch, NDrawer, NDrawerContent, NSelect } from 'naive-ui'
import { NFormItemRow, NInput, NForm, NDatePicker } from 'naive-ui'
import { apiConfig } from "@/apiConfig";

const errors = ref([])
const useStore = useUserStore()
const personalLink = reactive({})
const personalAllLink = reactive({})
const editing = reactive([])
const activeDrawerLinkEdit = ref(false)
const activeDrawerLinkAdd = ref(false)
const placementDrawer = ref('right')

const newLink = reactive({
  link: "",
  description: "",
  footnote: "",
  startDate: null,
  endDate: null,
  startDateStr: null,
  endDateStr: null,
  user: useStore.id,
})

const originalLink = reactive({
  link: "",
  description: "",
  footnote: "",
  startDate: null,
  endDate: null,
  startDateStr: null,
  endDateStr: null,
  user: useStore.id,
});

const editLink = reactive({
  link: "",
  description: "",
  footnote: "",
  startDate: null,
  endDate: null,
  startDateStr: null,
  endDateStr: null,
  user: useStore.id,
})

const columns = ref([
    {
      title: 'link',
      key: 'link'
    },
    {
      title: 'click',
      key: 'click'
    },
    {
      title: 'Edit',
      key: 'Edit',
      render: () => 'Edit'
    },
])

const columnsAll = ref([
    {
      title: 'link',
      key: 'link'
    },
    {
      title: 'click',
      key: 'click'
    },
])

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function switchAddLink(){
    activeDrawerLinkAdd.value = !activeDrawerLinkAdd.value
}

function truncateUrl(url, length = 30) {
    return url.length > length ? url.substring(0, length) + "..." : url;
}

async function getProject () {
  console.log('getProject')
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

async function addData() {
  errors.value = []
  try {
    console.log('addData')
    console.log('NEWdate',newLink)
    newLink.startDate = formatDate(new Date(newLink.startDateStr))
    newLink.endDate = formatDate(new Date(newLink.endDateStr))
    console.log('NEWdate',JSON.stringify(newLink))
    const { data, pending, refresh, error } = await useFetch('/api/personalLink/', {
        method: 'POST',
        baseURL:apiConfig.API_ENDPOINT,
        headers: {
        Authorization: `JWT ${useStore.token}`,
        },
        body: JSON.stringify(newLink)
    })

    if (data.value) {
        console.log('NEWdate data.value',data.value)
        getProject()
        switchAddLink()
    } else {
        console.log('error',error)
        errors.value.push(error.value.data)
    }
  } catch (error) {
    console.error('Error deleting data:', error);
  }
}

onMounted(() => {
  getProject()
})

</script>

<template>
  <indexHead />
  <div class="py-10 px-6 defalutBackground">
    <div class="space-y-4">
        test
    </div>
  </div>

</template>

<style scoped>
.defalutBackground {
  background: rgba(0, 104, 189, 0.2);
  padding: 24px;
}
</style>