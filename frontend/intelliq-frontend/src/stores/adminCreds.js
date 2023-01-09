import { defineStore } from 'pinia'
import { watch, reactive, computed } from 'vue'
export const useAdminStore = defineStore('adminCreds', () => {
    const admin = reactive({
        name: null,
        accessToken: null
    })
    const adminInStorage = localStorage.getItem('admin')
    if (adminInStorage) {
        const { name, accessToken } = JSON.parse(adminInStorage)
        admin.name = name
        admin.accessToken = accessToken
    }
    watch(() => admin, (state) => {
        localStorage.setItem('admin', JSON.stringify(state))
    }, { deep: true })
    const username = computed(() => admin.name)
    const token = computed(() => admin.accessToken)
    function setBoth(usr, tkn) {
        admin.name = usr
        admin.accessToken = tkn
    }
    function clearBoth() {
        admin.name = null
        admin.accessToken = null
    }
    return { admin, username, token, setBoth, clearBoth }
})