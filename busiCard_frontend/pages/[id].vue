<script setup>
import { apiConfig } from "@/apiConfig";
import { NDivider, NWatermark, NEllipsis, NAvatar, NForm, NImage } from 'naive-ui'

const route = useRoute()

const { id } = route.params

const backgroundColor = ref('#0068bd33');
const personalLink = reactive({})
const personalAllLink = reactive({})
const personalProfile = reactive({})

async function getPerson () {
//   console.log('getPerson',`/api/businessCard/?auth=${id}`)
  try{
      const data  = await $fetch(`/api/businessCard/?auth=${id}`, {
          method: 'GET',
          baseURL:apiConfig.API_ENDPOINT,
      })
    //   console.log('datagetPerson',data)
      if (data) {
        // console.log('personalProfile', data.results[0])
        Object.assign(personalProfile, data.results[0])
        // console.log('personalProfile',personalProfile)
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
        //   console.log('personalLink',personalLink)
      } else {
        //   console.log('errorgetLinks',error)
          errors.value.push(error.value.data)
      }
  } catch (err) {
      console.log('err',err)
  }
}

async function handleLinkClick(linkId) {
    // console.log('handleLinkClick',linkId)
    const ip = '...' // Retrieve the user's IP address here
    const { data, pending, refresh, error } = await useFetch('/api/linkClick/', {
        method: 'POST',
        baseURL: apiConfig.API_ENDPOINT,

        body: JSON.stringify({
            link_id: linkId,
            ip: ip
            }),
    })
}

onMounted(() => {
  getPerson()
})

</script>

<template>
    <n-watermark
    v-model:content="personalProfile.name"
    cross
    fullscreen
    :font-size="64"
    :line-height="64"
    :width="400"
    :height="284"
    :x-offset="12"
    :y-offset="60"
    :rotate="-15"
    />
    <div class="py-10 px-6" :style="{ background: backgroundColor }">
        <div class="space-y-4 text-center items-center justify-between">
            <!-- {{personalProfile}} -->
            <n-form>
                <div class="space-y-2">
                    <div>
                        <n-avatar
                            v-if="personalProfile.logo"
                            round
                            :size="168"
                            v-model:src="personalProfile.logo"
                        />
                    </div>

                    <n-ellipsis expand-trigger="click" line-clamp="2" :tooltip="false">
                        <div class="font-bold text-gray-600">
                            {{ personalProfile.description }}
                        </div> 
                    </n-ellipsis>
                     
                </div>   
            </n-form>
            <n-divider />
            <n-form>
                <div class="space-y-2">
                    <ul v-for="item in personalAllLink" :key="item.id">
                        <NuxtLink :to="item.link" @click="handleLinkClick(item.id)">
                            <div class="text-gray-700 rounded-xl font-semibold">
                                <div class="text-lg hover:bg-pink-200">
                                    {{ item.description }}
                                </div>
                                <div>
                                    <n-image
                                        v-if="item.pic"
                                        width="200"
                                        v-model:src="item.pic"
                                    />
                                </div>
                            </div>
                        </NuxtLink>
                        <n-divider dashed/>
                    </ul>
                </div>
            </n-form>
            <!-- {{ personalAllLink }} -->
        </div>
    </div>
</template>

<style scoped>
.n-card {
  max-width: 300px;
}
</style>

