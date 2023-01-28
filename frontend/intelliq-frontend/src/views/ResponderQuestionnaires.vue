<template>
    <div>
        <h2>Available questionnaires:</h2>
        <table>
            <tr v-for="q in questions">
                <td>
                    {{ q[1] }}
                </td>
                <td>
                    <router-link :to="'/answer/' + q[0]">Answer!</router-link>
                </td>
            </tr>
        </table>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import axios from 'axios';

export default {
    name: "ResponderHome",
    data() {
        return {
            questions: [],
        }
    },
    methods: {
        async getQuestions() {
            axios.get("http://127.0.0.1:9103/getQuestionnaires",
                { headers: { "X-OBSERVATORY-AUTH": this.adminToken } }).then(
                    (response) => {
                        this.questions = response.data;

                    })
        }
    },
    async created() {
        this.getQuestions();
    }
}
</script>
