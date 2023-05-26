export const useUserStore = definePiniaStore('userStore', ()=>{
    
    const isAuthenticated = ref(false)
    const token = ref('')

    const id = ref('')
    const username = ref('')
    const email = ref('')
    const is_staff = ref(false)
    const is_superuser = ref(false)

    // Initialize the store from local storage if possible
    const initStore = () => {
        // console.log('Initialized user', localStorage)
        if (localStorage.getItem('token')) {
            token.value = localStorage.getItem('token') as string
            isAuthenticated.value = localStorage.getItem('isAuthenticated') === 'true'
            id.value = localStorage.getItem('id') as string
            username.value = localStorage.getItem('username') as string
            email.value = localStorage.getItem('email') as string
            is_staff.value = localStorage.getItem('is_staff') === 'true'
            is_superuser.value = localStorage.getItem('is_superuser') === 'true'

            // console.log('Initialized user token:', token.value)
        }
    }

    const setToken = (posttoken: string) => {
        // console.log('Setting token:', posttoken)
        isAuthenticated.value = true
        token.value = posttoken
        localStorage.setItem('token', posttoken) // Store the token in local storage
        localStorage.setItem('isAuthenticated', 'true')
        // console.log('Storage token:', localStorage)
        // console.log('Getting token:', localStorage.getItem('token'))
    };

    const removeToken = () => {
        // console.log('Removing token')
        isAuthenticated.value = false
        token.value = ''
        localStorage.removeItem('token') // Remove the token from local storage
        localStorage.removeItem('isAuthenticated')
        localStorage.removeItem('id')
        localStorage.removeItem('username')
        localStorage.removeItem('email')
        localStorage.removeItem('is_staff')
        localStorage.removeItem('is_superuser')
    }

    const setUserDetail = (POSTid: string,
        POSTusername: string,
        POSTemail: string,
        POSTis_staff: boolean,
        POSTis_superuser: boolean,) => {
        // console.log('Setting user detail:',POSTusername)
        id.value = POSTid
        username.value = POSTusername
        email.value = POSTemail
        is_staff.value = POSTis_staff
        is_superuser.value = POSTis_superuser

        localStorage.setItem('id', POSTid)
        localStorage.setItem('username', POSTusername)
        localStorage.setItem('email', POSTemail)
        localStorage.setItem('is_staff', POSTis_staff.toString())
        localStorage.setItem('is_superuser', POSTis_superuser.toString())
    }

    const getUserDetail = () => {
        // console.log("Getting user detail", id.value);
        return {
            id: id.value,
            username: username.value,
            email: email.value,
            is_staff: is_staff.value,
            is_superuser: is_superuser.value,
        };
    }

    const removeUserDetail = () => {
        // console.log('Removing user detail')
        id.value = ''
        username.value = ''
        email.value = ''
        is_staff.value = false
        is_superuser.value = false
    }

    return {
        isAuthenticated,
        token,
        id,
        username,
        email,
        is_staff,
        is_superuser,
        setToken,
        removeToken,
        setUserDetail,
        removeUserDetail,
        getUserDetail,
        initStore
    }
})

 