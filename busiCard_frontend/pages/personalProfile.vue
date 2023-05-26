<script setup>
import {NButton,NForm, NFormItemRow, NInput, NSwitch, NColorPicker, NDivider, NUpload, NImage} from 'naive-ui'
import { apiConfig } from "@/apiConfig";
const useStore = useUserStore()

const result = reactive({})
const errors = ref([])
const personalProfile = reactive({})
const authProfile = reactive({})
const authProfileOrigin = reactive({})

const editPersonal = ref(false)

function resetColor () {
  personalProfile.color = '#0068bd33'
}

async function getProject () {
//   console.log('getProject')
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
        //   console.log('personalProfile',personalProfile)
      } else {
          console.log('error',error)
      }
  } catch (err) {
      console.log('err',err)
  }
}

async function getAuth () {
//   console.log('getAuth')
  try{
      const { data, pending, refresh, error } = await useFetch(`/api/regist/${useStore.id}`, {
          method: 'GET',
          baseURL:apiConfig.API_ENDPOINT,
          headers: {
              Authorization: `JWT ${useStore.token}` 
          }
      })
    //   console.log('data',data)
      if (data.value) {
          Object.assign(authProfile, data.value)
          Object.assign(authProfileOrigin, data.value)
        //   console.log('authProfile',authProfile)
      } else {
          console.log('error',error)
      }
  } catch (err) {
      console.log('err',err)
  }
}

async function createPerson () {
    resetColor()
    // console.log('createPerson')
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
              description: personalProfile.description,
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

const handleLogoUpload = async (file, fileList) => {
    // Create a FormData object
    let formData = new FormData();

    // Append file to formData object
    formData.append('file', file.raw);

    // Use useFetch to send the file to the server
    const { data, error } = await useFetch(`/api/upload/logo/`, {
        method: 'POST',
        baseURL: apiConfig.API_ENDPOINT,
        headers: {
            Authorization: `JWT ${useStore.token}`
        },
        body: formData
    });

    if (data.value) {
        // The file upload was successful
        console.log('File upload successful');
    } else {
        // There was an error uploading the file
        console.log('Error uploading file: ', error);
    }
}



async function updateAuth () {
  console.log('updateAuth')
  const updatedFields = {}
  for (const key in authProfile) {
      if (authProfile[key] !== authProfileOrigin[key]) {
          updatedFields[key] = authProfile[key];
      }        
  }
//   console.log('updatedFields',updatedFields)
  try {
      const { data, pending, refresh, error } = await useFetch(`/api/regist/${useStore.id}/`, {
          method: 'PATCH',
          baseURL:apiConfig.API_ENDPOINT,
          headers: {
              Authorization: `JWT ${useStore.token}` 
          },
          body: JSON.stringify(updatedFields),
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
  getAuth()
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

        <n-form-item-row label="顯示名稱">
          <n-input clearable :disabled="!editPersonal" placeholder="What name do you want to show" v-model:value="personalProfile.name" />
        </n-form-item-row>
        <n-form-item-row label="顯示訊息" v-if="personalProfile.id">
          <n-input clearable :disabled="!editPersonal" placeholder="What message U want to show" v-model:value="personalProfile.description" />
        </n-form-item-row>
        <n-form-item-row label="logo" v-if="personalProfile.id">
          <n-image v-if="personalProfile.logo" width="600" v-model:src="personalProfile.logo" />
          <n-upload
          :action="`${apiConfig.API_ENDPOINT}/api/upload/logo/`"
          :headers="{
              Authorization: `JWT ${useStore.token}`
          }"
          list-type="image-card"
          @file-change="handleLogoUpload"
          :disabled="!editPersonal"
          accept="image/jpeg, image/png, image/gif, image/bmp, image/webp, image/svg+xml, image/tiff, image/x-icon, image/vnd.microsoft.icon"
          >
            上傳個人logo
          </n-upload>
        </n-form-item-row>
        <n-form-item-row label="background" v-if="personalProfile.id">
        </n-form-item-row>
        
        <n-form inline v-if="personalProfile.id">        
          <n-form-item-row inline label="color" >
              <n-color-picker :modes="['hex']" :disabled="!editPersonal" v-model:value="personalProfile.color" />
          </n-form-item-row>
          <n-form-item-row>
            <n-button v-if="editPersonal" :disabled="!editPersonal" type="default" round block secondary strong @click="resetColor">
              reset Color
            </n-button>            
          </n-form-item-row>
        </n-form>          

        <div v-if="errors.length" class="mb-6 py-4 px-6 bg-rose-400 rounded-xl">
            <p v-for="error in errors" :key="error">
                {{ error }}
            </p>
        </div>
        <n-button :disabled="!editPersonal" v-if="personalProfile.id" type="info" block secondary strong @click="updatePerson">
            修改
        </n-button>
        <n-button :disabled="!editPersonal" v-if="!personalProfile.id" type="info" block secondary strong @click="createPerson">
            新增
        </n-button>

        <n-divider />
        <div v-if="editPersonal">
          <n-form-item-row label="帳號名稱">
          <n-input clearable :disabled="!editPersonal" placeholder="What name do you want to show" v-model:value="authProfile.username" />
          </n-form-item-row>
          <n-form-item-row label="密碼">
            <n-input clearable type="password" :disabled="!editPersonal" placeholder="What name do you want to show" v-model:value="authProfile.password" />
          </n-form-item-row> 
          <n-form-item-row label="Email">
            <n-input clearable :disabled="!editPersonal" placeholder="What name do you want to show" v-model:value="authProfile.email" />
          </n-form-item-row>      
          <n-button type="info" block secondary strong @click="updateAuth">
              修改
          </n-button>        
        </div>

        



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