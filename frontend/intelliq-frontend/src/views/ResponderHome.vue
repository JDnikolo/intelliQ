<script>
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
            console.log("Getting Questions")
            axios.get("http://127.0.0.1:5000/questionnaire/QQ000",
                config = { headers: { "X-OBSERVATORY-AUTH": "e00f8e21a864de304a6c" } }).then(
                    (response) => {
                        this.questions = response.data.questions;
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
        <h1>Test me</h1>
        <div v-for="q in questions">
            {{ q }}
        </div>
    </div>
</template>