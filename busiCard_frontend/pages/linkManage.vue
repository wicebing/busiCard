<script setup>
import { NButton, NTabs, NTabPane, NSwitch, NDrawer, NDrawerContent, NImage, NUpload } from 'naive-ui'
import { NFormItemRow, NInput, NForm, NDatePicker } from 'naive-ui'
import { apiConfig } from "@/apiConfig";

const errors = ref([])
const useStore = useUserStore()
const personalLink = reactive({})
const personalAllLink = reactive({})
const editing = reactive([])
const editingAll = reactive([])
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
  sequence: 0,
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
  sequence: 0,
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
  sequence: 0,
})

const columns = ref([
    {
      title: 'link',
      key: 'link'
    },
    {
      title: 'VC',
      key: 'unique_clicks'
    },
    {
      title: 'AC',
      key: 'total_clicks'
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
])

const columnsAll = ref([
    {
      title: 'link',
      key: 'link'
    },
    {
      title: 'VC',
      key: 'unique_clicks'
    },
    {
      title: 'AC',
      key: 'total_clicks'
    },
    {
      title: 'Edit',
      key: 'Edit',
    },
    {
      title: 'Delete',
      key: 'Delete',
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

function convertStartDate(editLink) {
    console.log('convertDate', editLink.startDate)
  return computed({
    get: () => new Date(editLink.startDate).getTime(),
    set: (newValue) => (editLink.startDate = formatDate(new Date(newValue))),
  });
}

function convertEndDate(editLink) {
    console.log('convertDate', editLink.endDate)
  return computed({
    get: () => new Date(editLink.endDate).getTime(),
    set: (newValue) => (editLink.endDate = formatDate(new Date(newValue))),
  });
}

async function editData(row) {
    console.log("Row:", row)
    Object.assign(editLink, row)
    Object.assign(originalLink, row); // Store the original data before editing
    console.log("editProject:", editLink)
    activeDrawerLinkEdit.value = true
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
          console.log('today',today)

          // Filter personalLink where endDate is not before today
          const filteredPersonalLink = data.value.results.filter(link => {
              const endDate = new Date(link.endDate);
              const startDate = new Date(link.startDate);
              console.log('endDate',endDate)
              console.log('startDate',startDate)
              return endDate >= today && startDate <= today;
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

async function deleteData(row) {
    try {
        console.log('deleteData', row)
        const { data, pending, refresh, error } = await useFetch(`/api/personalLink/${row.id}`, {
          method: 'DELETE',
          baseURL:apiConfig.API_ENDPOINT,
          headers: {
          Authorization: `JWT ${useStore.token}`,
          },
        })

        console.log('deleteData', row)
        console.log('Deleted successfully')
        console.log('Error: ', error.value)
    } catch (error) {
        console.error('Error deleting data:', error);
    }
    getProject()
}

async function updateData() {
    console.log("Updating data:", editLink);
    const updatedFields = {}
    for (const key in editLink) {
        if (editLink[key] !== originalLink[key]) {
            updatedFields[key] = editLink[key];
            console.log("Updated fields key:", key);
        }        
    }
    console.log("Updated fields:", updatedFields);
    console.log(editLink.id)

    try {
        const { data, pending, refresh, error } = await useFetch(`/api/personalLink/${editLink.id}/`, {
            method: 'PATCH',
            baseURL:apiConfig.API_ENDPOINT,
            headers: {
            Authorization: `JWT ${useStore.token}`,
            },
            body: JSON.stringify(updatedFields),
        });

        console.log("Updated successfully:", data.value);
        getProject(); // Refresh the staff list after the update is successful
        activeDrawerLinkEdit.value = false;
    } catch (error) {
        console.error('Error updating data:', error);
    }
}

const handlePersonalLinkImageUpload = async (file, fileList) => {
  // Create a FormData object
  const formData = new FormData();
  // Append file to formData object
  formData.set('id', editLink.id)
  formData.append('file', file.raw);
  

  // Use useFetch to send the file to the server
  const { data, error } = await useFetch(`/api/upload/personalLinkImage/`, {
      method: 'POST',
      baseURL: apiConfig.API_ENDPOINT,
      headers: {
          Authorization: `JWT ${useStore.token}`
      },
      body: formData
  });
}

onMounted(() => {
  getProject()
})

</script>

<template>
  <indexHead />
  <div class="py-10 px-6 defalutBackground">
    <div class="space-y-4">
      <n-tabs
      type="segment"
      class="card-tabs"
      default-value="allActiveLink"
      size="small"
      animated
      pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;"
      >
        <n-tab-pane name="allActiveLink" tab="展示中">
          <n-button dashed type="warning" strong
          @click=switchAddLink
          >
              add Link
          </n-button>
          <div style="overflow-x: auto;">
            <table class="table-auto min-w-full">
              <thead class="bg-gray-50">
                  <tr>
                      <th v-for="col in columns" class="px-2 py-1 text-xs font-bold text-gray-500" scope="col">{{ col.title }}</th>
                  </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-for="(res, rowIndex) in personalLink">
                  <td v-for="col in columns" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                    <n-button 
                    v-if="!res[col.key] && col.title === 'Edit'"
                    secondary
                    type='info'
                    @click= editData(res)
                    >
                        {{ col.key }}
                    </n-button>

                    <div v-if="res[col.key] !== null && res[col.key] !== undefined ">
                      <div v-if="col.key === 'link'">
                        <ul>
                        <NuxtLink :to="res[col.key]">{{ truncateUrl(res[col.key],length=20) }}</NuxtLink>
                        </ul>
                        <ul class="bg-green-200">{{ truncateUrl(res['description'],length=10) }}</ul>
                        <ul class="bg-green-100">{{ truncateUrl(res['footnote'],length=10) }}</ul>
                        <ul class="bg-red-100">{{ res['startDate'] }} ~ {{ res['endDate'] }}</ul>
                      </div>
                      <div v-if="col.key === 'unique_clicks'">
                        {{ res[col.key] }}
                      </div>
                      <div v-if="col.key === 'total_clicks'">
                        {{ res[col.key] }}
                      </div>
                    </div>                              
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </n-tab-pane>
        <n-tab-pane name="allLink" tab="歷史">
          <table class="table-auto min-w-full">
            <thead class="bg-gray-50">
                <tr>
                    <th v-for="col in columnsAll" class="px-2 py-1 text-xs font-bold text-gray-500" scope="col">{{ col.title }}</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="(res, rowIndex) in personalAllLink">
                <td v-for="col in columnsAll" class="px-2 py-2 text-sm font-medium text-gray-800 whitespace-nowrap">
                  <div v-if="!res[col.key]  && col.title === 'Delete'">
                    <ul>
                      <n-button 
                      secondary strong type='error'
                      @click=deleteData(res)
                      :disabled="!editingAll[rowIndex]"
                      >
                          {{ col.key }}
                      </n-button>                      
                    </ul>
                    <ul>
                      <n-switch v-model:value="editingAll[rowIndex]" />
                    </ul>
                  </div>

                  <n-button 
                    v-if="!res[col.key] && col.title === 'Edit'"
                    secondary
                    type='info'
                    @click= editData(res)
                    >
                        {{ col.key }}
                    </n-button>
                  

                  <div v-if="res[col.key] !== null && res[col.key] !== undefined ">
                    <div v-if="col.key === 'link'">
                      <ul>
                        <NuxtLink :to="res[col.key]">{{ truncateUrl(res[col.key],length=12) }}</NuxtLink>
                      </ul>
                      <ul class="bg-green-200">{{ truncateUrl(res['description'],length=5) }}</ul>
                      <ul class="bg-green-100">{{ truncateUrl(res['footnote'],length=5) }}</ul>
                      <ul class="bg-red-100">{{ res['startDate'] }}</ul>
                      <ul class="bg-red-100">{{ res['endDate'] }}</ul>
                    </div>
                    <div v-if="col.key === 'unique_clicks'">
                      {{ res[col.key] }}
                    </div>
                    <div v-if="col.key === 'total_clicks'">
                        {{ res[col.key] }}
                    </div>
                  </div>                              
                </td>
              </tr>
            </tbody>
          </table>
        </n-tab-pane>
      </n-tabs>
    </div>
  </div>
  <n-drawer v-model:show="activeDrawerLinkAdd" :width="300" :placement="placementDrawer">
      <n-drawer-content title="新增Link" closable>
          <n-form>
              <n-form-item-row label="link">
                  <n-input placeholder="link" v-model:value="newLink.link" />
              </n-form-item-row>
              <n-form-item-row label="description">
                  <n-input placeholder="description" v-model:value="newLink.description" />
              </n-form-item-row>
              <n-form-item-row label="footnote">
                  <n-input placeholder="footnote" v-model:value="newLink.footnote" />
              </n-form-item-row>
              <n-form-item-row label="sequence">
                  <n-input placeholder="sequence" v-model:value="newLink.sequence" />
              </n-form-item-row>
              <n-form-item-row label="startDate">
                  <n-date-picker type="date"  v-model:value="newLink.startDateStr" />
              </n-form-item-row>
              <n-form-item-row label="endDate">
                  <n-date-picker type="date"  v-model:value="newLink.endDateStr" />
              </n-form-item-row>
              <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
                  <p v-for="error in errors">
                    {{ error }}
                  </p>
              </div>
              <n-button type="primary" block secondary strong @click="addData">
              新增
              </n-button>
          </n-form>
      </n-drawer-content>
  </n-drawer>
  <n-drawer v-model:show="activeDrawerLinkEdit" :width="300" :placement="placementDrawer">
      <n-drawer-content title="修改Link" closable>
          <n-form>
              <n-form-item-row label="link">
                  <n-input placeholder="link" v-model:value="editLink.link" />
              </n-form-item-row>
              <n-form-item-row label="description">
                  <n-input placeholder="description" v-model:value="editLink.description" />
              </n-form-item-row>
              <n-form-item-row label="footnote">
                  <n-input placeholder="footnote" v-model:value="editLink.footnote" />
              </n-form-item-row>
              <n-form-item-row label="sequence">
                  <n-input placeholder="sequence" v-model:value="editLink.sequence" />
              </n-form-item-row>
              <n-form-item-row label="startDate">
                  <n-date-picker type="date"  v-model:value="convertStartDate(editLink).value" />
              </n-form-item-row>
              <n-form-item-row label="endDate">
                  <n-date-picker type="date"  v-model:value="convertEndDate(editLink).value" />
              </n-form-item-row>
              <n-form-item-row label="pic">
                <n-image v-if="editLink.pic" width="200" v-model:src="editLink.pic"/>
                <n-upload 
                  :action="`${apiConfig.API_ENDPOINT}/api/upload/personalLinkImage/`"
                  :headers="{
                    Authorization: `JWT ${useStore.token}`
                  }"
                  :data="{
                    id: editLink.id
                  }"
                  list-type="image-card"
                  :on-finish="getProject">
                  上傳image
                </n-upload>
              </n-form-item-row>
              <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
                  <p v-for="error in errors">
                    {{ error }}
                  </p>
              </div>
              <n-button type="primary" block secondary strong @click="updateData">
              修改
              </n-button>
          </n-form>
      </n-drawer-content>
  </n-drawer>
</template>

<style scoped>
.defalutBackground {
  background: rgba(0, 104, 189, 0.2);
  padding: 24px;
}
</style>