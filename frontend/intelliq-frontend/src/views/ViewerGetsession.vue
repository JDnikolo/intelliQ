<script>
import { RouterLink } from 'vue-router';
import { useViewerStore } from '../stores/viewerCreds.js'
import axios from 'axios';

export default {
    name: "ViewerGetsession",
    setup() {
        const store = useViewerStore()
        return { store, }
    },
    data() {
        return {
            sessions: [],
            sanswers: {
                "answers":
                {
                    "qID": "",
                    "ans": ""
                }
            },
            selected: null,
        }
    },
    props: {
        qnrID: String,
    },
    methods: {
        async getSessions(id) {
            console.log("Getting Sessions")
            axios.get("http://127.0.0.1:9103/getSessions/" + id,
                { headers: { "X-OBSERVATORY-AUTH": this.adminToken } }).then(
                    (response) => {
                        this.sessions = response.data;

                    })
        },
        isSelected(q) {
            return q === this.selected
        },
        /*setSelected(q) {
            if (this.selected === q) {
                this.selected = null;
            } else {
                this.selected = q;
            }
        },*/
        setSelected(q) { this.selected = q; },
        async getSessionAnswers(id, sessionID) {
            console.log("Getting Session Answers")
            let token = this.store.token
            axios.get("http://127.0.0.1:9103/intelliq_api/getsessionanswers/" + id + "/" + sessionID,
                { headers: { "X-OBSERVATORY-AUTH": token } }).then(
                    (response) => {
                        this.sanswers = response.data;

                    })
        }
    },
    async created() {
        console.log('mounting');
        this.getSessions(this.qnrID);
    }
}
</script>
<template>
    <div style="background-color:#93CAED">
        <p><u>Available sessions for {{ this.qnrID }}:</u></p>
        <!-- <table>
            <tr v-for="s in sessions" @click="setSelected(s)">
                <td :class="{ selected: isSelected(s) }">
                    {{ s[0] }}
                </td>
            </tr>
        </table> -->

        <select name="available" id="sess" v-model="selected">
            <option disabled selected value>--Select a session--</option>
            <option v-for="s in sessions" :value="s">
                {{ s[0] }}
            </option>
        </select>

        <button :disabled="selected == null" @click="getSessionAnswers(this.qnrID, selected[0])">
            Session answers:
        </button>

        <table style="border: 1px solid black; border-collapse: collapse;">
            <th>Answers of session:</th>
            <tr v-for="i in sanswers.answers.length">
                <td style="border: 1px solid black;"> {{ sanswers.answers[i - 1].qID }} </td>
                <td style="border: 1px solid black;"> {{ sanswers.answers[i - 1].ans }} </td>
            </tr>
        </table>
    </div>
</template>

<style scoped>
.selected {
    color: green;
    font-weight: bold;
}

th {
    font-weight: bold;
}
</style>