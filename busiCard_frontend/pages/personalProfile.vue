<script setup>
import {NButton,NForm, NFormItemRow, NInput, NSwitch, NColorPicker, } from 'naive-ui'
import { apiConfig } from "@/apiConfig";
const useStore = useUserStore()

const result = reactive({})
const errors = ref([])
const personalProfile = reactive({})

const editPersonal = ref(false)

function resetColor () {
  personalProfile.color = '#0068bd33'
}

async function getProject () {
  console.log('getProject')
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
      } else {
          console.log('error',error)
      }
  } catch (err) {
      console.log('err',err)
  }
}

async function createPerson () {
  console.log('createPerson')
  errors.value = []
  try{
      const { data, pending, refresh, error } = await useFetch(`/api/businessCard/`, {
          method: 'POST',
          baseURL:apiConfig.API_ENDPOINT,
          headers: {
              Authorization: `JWT ${useStore.token}` 
          },
          body: {
              name: personalProfile.name,
              user: useStore.id,
              color: personalProfile.color,
          }
      })
      if (data.value) {
          Object.assign(personalProfile, data.value)
      } else {
          console.log('error',error)
          errors.value.push(error.value.data)
      }
  } catch (err) {
      console.log('err',err)
  }
}

async function updatePerson () {
  try {
      const { data, pending, refresh, error } = await useFetch(`/api/businessCard/${personalProfile.id}/`, {
          method: 'PATCH',
          baseURL:apiConfig.API_ENDPOINT,
          headers: {
              Authorization: `JWT ${useStore.token}` 
          },
          body: {
              name: personalProfile.name,
              user: useStore.id,
              color: personalProfile.color,
          }
      })
      if (data.value) {
      } else {
          console.log('error',error)
          errors.value.push(error.value.data)
      }
  } catch (err) {
      console.log('err',err)
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
      <n-form>
        <span class="text-green-800 font-black"> 修改資料</span>
        
        <n-switch v-model:value="editPersonal" />
        <n-form inline> </n-form>
        <n-form-item-row label="名稱">
          <n-input :disabled="!editPersonal" placeholder="What name do you want to show" v-model:value="personalProfile.name" />
        </n-form-item-row>
        <n-form-item-row label="logo">
        </n-form-item-row>
        <n-form-item-row label="background">
        </n-form-item-row>
        
        <n-form inline>        
          <n-form-item-row inline label="color" >
              <n-color-picker :modes="['hex']" :disabled="!editPersonal" v-model:value="personalProfile.color" />
          </n-form-item-row>
          <n-form-item-row>
            <n-button v-if="editPersonal" type="default" round block secondary strong @click="resetColor">
              reset Color
            </n-button>            
          </n-form-item-row>
        </n-form>          

        <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
            <p v-for="error in errors" :key="error">
                {{ error }}
            </p>
        </div>
        <n-button v-if="personalProfile.id" type="info" block secondary strong @click="updatePerson">
            更正
        </n-button>
        <n-button v-if="!personalProfile.id" type="info" block secondary strong @click="createPerson">
            新增
        </n-button>     
      </n-form>
    </div>
  </div>
</template>

<style scoped>
.defalutBackground {
  background: rgba(0, 104, 189, 0.2);
  padding: 24px;
}
</style>