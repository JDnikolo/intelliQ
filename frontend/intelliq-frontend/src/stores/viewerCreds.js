import { defineStore } from 'pinia'
import { watch, reactive, computed } from 'vue'
export const useViewerStore = defineStore('viewerCreds', () => {
    const user = reactive({
        name: null,
        accessToken: null
    })
    const userInStorage = localStorage.getItem('user')
    if (userInStorage) {
        const { name, accessToken } = JSON.parse(userInStorage)
        user.name = name
        user.accessToken = accessToken
    }
    watch(() => user, (state) => {
        localStorage.setItem('user', JSON.stringify(state))
    }, { deep: true })
    const username = computed(() => user.name)
    const token = computed(() => user.accessToken)
    function setBoth(usr, tkn) {
        user.name = usr
        user.accessToken = tkn
    }
    function clearBoth() {
        user.name = null
        user.accessToken = null
    }
    return { user, username, token, setBoth, clearBoth }
})