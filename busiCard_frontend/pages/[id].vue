<script setup>
import { apiConfig } from "@/apiConfig";
import { NDivider, NWatermark, NCard, NAvatar, NSpace, NForm, NImage } from 'naive-ui'

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
    <n-watermark
    v-model:content="personalProfile.name"
    cross
    fullscreen
    :font-size="64"
    :line-height="64"
    :width="284"
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
                    <n-avatar
                        v-if="personalProfile.logo"
                        round
                        size="large"
                        v-model:src="personalProfile.logo"
                    />
                    <div>
                        personalProfile description
                    </div>                      
                </div>   
            </n-form>
            <n-divider />
            <n-form>
                <div class="space-y-2">
                    <ul v-for="item in personalAllLink" :key="item.id">
                        <NuxtLink :to="item.link">
                            <div class="text-lg">
                                {{ item.description }}
                            </div>
                            <div>
                                <n-image
                                    v-if="item.pic"
                                    width="100"
                                    src="https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg"
                                />
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

