<template>
    <header>
        <span>Welcome, {{ this.store.username }}</span>
        <span>
            <button @click="logout()">Logout</button>
        </span>
    </header>
    <div>Select a questionnaire to perform administrative action.</div>
    <div>Available questionnaires:
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
        <button :disabled="selected == null" @click="$router.push('/admin/endpoints/resetq/'+selected[0])">
            Reset Questionnaire Answers
        </button>
        <button :disabled=true>
            Reset All Answers (inactive)
        </button>
		<router-view :key="$route.path"></router-view> <!-- This line shows stuff on same page. Without it, nothing -->
    </div>
</template>
<script>
import { useAdminStore } from '../stores/adminCreds.js'
import axios from 'axios'
export default {
    name: "AdminEndpoints",
    setup() {
        const store = useAdminStore()
        return { store, }
    },
    data() {
        return {
            questionnaires: [],
            selected: null,
        }
    },
    methods: {
        logout() {
            let token = this.store.token
            axios.post("http://127.0.0.1:9103/intelliq_api/logout", '', { headers: { "X-OBSERVATORY-AUTH": token } }).then((response) => {
                this.store.clearBoth()
                this.$router.push("/admin")
            }).catch((error) => {
                console.log(error)
                if (error.status == 400) {
                    this.message = "Incorrect Credentials"
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
        }
    },
    created() {
        if (this.store.token == null) {
            this.$router.replace("/admin")
        }
        axios.get("http://127.0.0.1:9103/getQuestionnaires",
            { headers: { "X-OBSERVATORY-AUTH": "e00f8e21a864de304a6c" } }).then(
                (response) => {
                    this.questionnaires = response.data;
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