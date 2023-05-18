export const useUserStore = definePiniaStore('userStore', ()=>{
    
    const isAuthenticated = ref(false)
    const token = ref('')

    const id = ref('')
    const username = ref('')
    const email = ref('')
    const is_staff = ref(false)
    const is_superuser = ref(false)

    // const initStore = () => {
    //     isAuthenticated.value = false
    //     if (localStorage.getItem('user.token')) {
    //         isAuthenticated.value = true
    //         token.value = localStorage.getItem('user.token')

    //         console.log('Initialized user:')
    //     }
    // }

    const setToken = (posttoken: string) => {
        console.log('Setting token:', posttoken)
        isAuthenticated.value = true
        token.value = posttoken
        // localStorage.setItem('token', posttoken)
    };

    const removeToken = () => {
        console.log('Removing token')
        isAuthenticated.value = false
        token.value = ''
        // localStorage.removeItem('user.token')
    }

    const setUserDetail = (POSTid: string,
        POSTusername: string,
        POSTemail: string,
        POSTis_staff: boolean,
        POSTis_superuser: boolean,) => {
        console.log('Setting user detail:',POSTusername)
        id.value = POSTid
        username.value = POSTusername
        email.value = POSTemail
        is_staff.value = POSTis_staff
        is_superuser.value = POSTis_superuser

    }

    const getUserDetail = () => {
        console.log("Getting user detail", id.value);
        return {
            id: id.value,
            username: username.value,
            email: email.value,
            is_staff: is_staff.value,
            is_superuser: is_superuser.value,
        };
    }

    const removeUserDetail = () => {
        console.log('Removing user detail')
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
        getUserDetail
    }
})
    
//     {
//     id: 'user',
//     state: () => ({
//         user:{
//             isAuthenticated: false,
//             email: null,
//             token: null
//         }
//     }),
//     getters: {
//         isAuthenticated: (state) => state.isAuthenticated,
//         name: (state) => state.name,
//         email: (state) => state.email,
//         token: (state) => state.token
//     },
//     actions: {
//         initStore() {
//             this.user.isAuthenticated false
//             if (localStorage.gerItem('user.token')) {
//                 this.user.isAuthenticated = true
//                 this.user.email = localStorage.getItem('user.email')
//                 this.user.token = localStorage.getItem('user.token')

//                 console.log('Initialized user:', this.user)
//             }
//         },
//         setToken(token, email) {
//             console.log('Setting token:', token, email)
//             this.user.isAuthenticated = true
//             this.user.email = email
//             this.user.token = token
//             localStorage.setItem('user.token', token)
//             localStorage.setItem('user.email', email)
//         },
//         removeToken() {
//             console.log('Removing token')
//             this.user.isAuthenticated = false
//             this.user.email = null
//             this.user.token = null
//             localStorage.removeItem('user.token')
//             localStorage.removeItem('user.email')
//         }
//     }
// })

