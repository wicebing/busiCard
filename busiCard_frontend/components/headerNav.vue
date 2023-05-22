<script setup>
import { NIcon, NDropdown, NButton } from 'naive-ui'
const useStore = useUserStore()
const useRoute = useRouter()

const options= ref([
        {
          label: '人員',
          key: 'userStaff',
          props: {
            onClick: () => {
              // message.success('Good!')
            }
          }
        },
        {
          label: '專案',
          key: 'projects',
          props: {
            onClick: () => {
            //   message.success('Good!')
            // useRoute.push('/projects')
            }
          }
        },
      ])

const optionsUser= ref([
        {
          label: '個人資料',
          key: 'personalProfile',
          props: {
            onClick: () => {
            //   message.success('Good!')
            navigateTo('/personalProfile')
            }
          }
        },
        {
          label: '連結管理',
          key: 'linkManage',
          props: {
            onClick: () => {
            //   message.success('Good!')
            navigateTo('/linkManage')
            }
          }
        },
      ])

function toBusiCard() {
  navigateTo(`/${useStore.username}`)
}

</script>

<template>
    <div v-if=useStore.isAuthenticated class="flex items-center space-x-4 font-bold font-mono">
        <n-dropdown v-if=useStore.is_superuser trigger="hover" :options="options">
            <span class="text-sky-800 hover:text-white">管理</span>
        </n-dropdown>
        <n-dropdown v-if=useStore.isAuthenticated trigger="hover" :options="optionsUser">
            <span class="text-sky-800 hover:text-white">個人</span>
        </n-dropdown>
        <n-button class="py-2 px-2 text-black rounded-xl font-semibold" :on-click="toBusiCard">預覽</n-button>

    </div>
</template>