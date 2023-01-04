<script>
import { RouterLink } from 'vue-router';
import axios from 'axios';
import { onMounted } from 'vue';

export default {
    name: "ResponderHome",
    data() {
        return {
            questions: [],
        }
    },
    methods: {
        async getQuestions() {
            console.log("Getting Questions")
            axios.get("http://127.0.0.1:9103/getQuestionnaires",
                { headers: { "X-OBSERVATORY-AUTH": "e00f8e21a864de304a6c" } }).then(
                    (response) => {
                        this.questions = response.data;

                    })
        }
    },
    async created() {
        console.log('mounting');
        this.getQuestions();
    }
}
</script>
<template>
    <div>
        <h1>Welcome to Intelliq</h1>
        <div>Available questionnaires:</div>
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