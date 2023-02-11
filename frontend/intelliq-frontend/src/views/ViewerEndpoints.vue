<template>
    <h3>
        <span>Welcome, {{ this.store.username }}</span>
        <span>
            <button @click="logout()">Logout</button>
        </span>
    </h3>
    <div>{{ message }}</div>
    <div>Select a questionnaire to view its results.</div>
    <div>
        <h2>Available questionnaires:</h2>
        <table>
            <th>QuestionnaireID</th>
            <th>Questionnaire Name</th>
            <tr v-for="q in questionnaires" @click="setSelected(q)">
                <td :class="{ selected: isSelected(q) }">
                    {{ q[0] }}
                </td>
                <td :class="{ selected: isSelected(q) }">{{ q[1] }}</td>
            </tr>
        </table>
		<button :disabled="selected == null"
            @click="$router.push('/viewer/endpoints/generalreview/' + selected[0])">
            General Review
        </button>
        <button :disabled="selected == null"
            @click="$router.push('/viewer/endpoints/getsessionanswers/' + selected[0])">
            Get Session Answers
        </button>
        <button :disabled="selected == null"
            @click="$router.push('/viewer/endpoints/getquestionanswers/' + selected[0])">
            Get Question Answers
        </button>
        <button :disabled="selected == null" @click="$router.push('/viewer/endpoints/getallanswers/' + selected[0])">
            Get All Answers
        </button>
        <router-view :key="$route.path"></router-view> <!-- This line shows stuff on same page. Without it, nothing -->
    </div>
</template>
<script>
import { useViewerStore } from '../stores/viewerCreds.js'
import axios from 'axios'
export default {
    name: "ViewerEndpoints",
    setup() {
        const store = useViewerStore()
        return { store, }
    },
    data() {
        return {
            message: '',
            questionnaires: [],
            selected: null,
        }
    },
    methods: {
        logout() {
            let token = this.store.token
            axios.post("http://127.0.0.1:9103/intelliq_api/logout", '', { headers: { "X-OBSERVATORY-AUTH": this.store.token } }).then((response) => {
                this.store.clearBoth()
                this.$router.push("/viewer")
            }).catch((error) => {
                if (error.response) {
                    if (error.response.status == 401) {
                        this.message = "Your credentials are no longer valid. Redirecting..."
                        this.store.clearBoth()
                        this.redirect()
                    }
                } else {
                    console.log(error)
                }
            })
        },
        isSelected(q) {
            return q === this.selected
        },
        setSelected(q) {
            if (this.selected === q) {
                this.selected = null;
            } else {
                this.selected = q;
            }
        },
        async redirect() {
            await new Promise(r => setTimeout(r, 2000));
            this.$router.replace("/viewer")
        }
    },
    created() {
        if (this.store.token == null) {
            this.$router.replace("/viewer")
        }
        axios.get("http://127.0.0.1:9103/getQuestionnaires",
            { headers: { "X-OBSERVATORY-AUTH": this.store.token } }).then(
                (response) => {
                    this.questionnaires = response.data;
                }).catch((error) => {
                    if (error.response) {
                        if (error.response.status == 401) {
                            this.message = "Your credentials are no longer valid. Redirecting..."
                            this.store.clearBoth()
                            this.redirect()
                        }
                    } else {
                        console.log(error)
                    }
                })
    }
}
</script>
<style scoped>
.selected {
    color: green;
    font-weight: bold;
}
</style>