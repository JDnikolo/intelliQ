<script>
import { RouterLink } from 'vue-router';
import { useViewerStore } from '../stores/viewerCreds.js'
import axios from 'axios';

export default {
    name: "ViewerGetquestion",
    setup() {
        const store = useViewerStore()
        return { store, }
    },
    data() {
        return {
            questions: [],
            qanswers: {
                "answers":
                {
                    "session": "",
                    "ans": ""
                }
            },
            selected: null,
			status_code: Number,
        }
    },
    props: {
        qnrID: String,
    },
    methods: {
        async getQuestions(id) {
            console.log("Getting Questions")
            axios.get("http://127.0.0.1:9103/getQuestions/" + id,
                { headers: { "X-OBSERVATORY-AUTH": this.store.token } }).then(
                    (response) => {
                        this.questions = response.data;

                    }).catch((error) => {
                        if (error.response) {
                            if (error.response.status == 401) {
                                this.store.clearBoth()
                                new Promise(r => setTimeout(r, 2000));
                                this.$router.replace("/viewer")
                            }
                        } else {
                            console.log(error)
                        }
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
        setSelected(q) { this.selected = q; console.log(q); },
        async getQuestionAnswers(id, questionID) {
            console.log("Getting question Answers")
            let token = this.store.token
            axios.get("http://127.0.0.1:9103/intelliq_api/getquestionanswers/" + id + "/" + questionID,
                { headers: { "X-OBSERVATORY-AUTH": token } }).then(
                    (response) => {
                        this.qanswers = response.data;
						this.status_code = response.status;
                    }).catch((error) => {
                        if (error.response) {
                            if (error.response.status == 401) {
                                this.store.clearBoth()
                                new Promise(r => setTimeout(r, 2000));
                                this.$router.replace("/viewer")
                            }
                        } else {
							this.status_code = error.response.status;
                            console.log(error)
                        }
                    })
        }
    },
    async created() {
        this.getQuestions(this.qnrID);
    }
}
</script>
<template>
    <div style="background-color:#93CAED">
        <p><u>Available questions for {{ this.qnrID }}:</u></p>
        <!-- <table>
            <tr v-for="s in questions" @click="setSelected(s)">
                <td :class="{ selected: isSelected(s) }">
                    {{ s[0] }}
                </td>
            </tr>
        </table> -->

        <select name="available" id="ques" v-model="selected">
            <option disabled selected value>--Select a question--</option>
            <option v-for="s in questions" :value="s">
                {{ s[0] }}
            </option>
        </select>

        <button :disabled="selected == null" @click="getQuestionAnswers(this.qnrID, selected[0])">
            Question answers:
        </button>

        <table style="border: 1px solid black; border-collapse: collapse;" v-if="status_code === 200">
            <th>Answers of question:</th>
            <tr v-for="i in qanswers.answers.length">
                <td style="border: 1px solid black;"> {{ qanswers.answers[i - 1].session }} </td>
                <td style="border: 1px solid black;"> {{ qanswers.answers[i - 1].ans }} </td>
            </tr>
        </table>
		<p v-else-if="status_code === 402"><i> This question has no answers yet! </i></p>
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