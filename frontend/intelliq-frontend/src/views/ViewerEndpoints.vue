<template>
    <header>
        Viewer Endpoints <span>Welcome, {{ this.store.username }}</span>

    </header>
</template>
<script>
import { useViewerStore } from '../stores/viewerCreds.js'
export default {
    name: "ViewerEndpoints",
    setup() {
        const store = useViewerStore()
        return { store, }
    },
    data() {
        return {
        }
    },
    methods: {
    },
    created() {
        console.log(this.store.username)
    }
}
</script>