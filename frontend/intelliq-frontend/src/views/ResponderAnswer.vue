<template>
    <div v-if="currentQuestion != null">
        <div>
            {{ parseQuestionText(currentQuestion.qtext) }}
        </div>
        <input v-if="isOpenQuestion" v-model="currentAnswer.opttxt" />
        <div v-if="!(isOpenQuestion)">
            <div v-for="opt in currentQuestion.options">
                <input type="radio" :id=opt.opttxt :value=opt v-model="currentAnswer" />
                <label :for=opt.opttxt>{{ opt.opttxt }}</label>
            </div>
        </div>
        <button :disabled="currentQuestion.required == 1">Skip</button>
        <button :disabled="hasAnswer" @click="addAnswer()">Answer</button>
    </div>
    <div v-if="completed">
        <h2>Thank you for your answers!</h2>
        <router-link to="/">Go Back</router-link>
        <table>
            <th>Question</th>
            <th>Answer</th>
            <tr v-for="ans in answers">
                <td>{{ parseQuestionText(ans.qtext) }}</td>
                <td>{{ ans.opttxt }}</td>
            </tr>
        </table>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: "ResponderAnswer",
    data() {
        return {
            currentQuestion: null,
            currentAnswer: null,
            nextQuestion: null,
            questions: [],
            answers: [],
            previousQuestions: {},
            previousOptions: {},
            session: null,
            completed: false,
        }
    },
    computed: {
        isOpenQuestion() {
            return this.currentQuestion.options[0].opttxt == "<open string>"
        },
        hasAnswer() {
            return (this.currentAnswer.optID == null || this.currentAnswer.opttxt == null || this.currentAnswer.opttxt == "")
        },
    },
    props: {
        qID: String,
    },
    methods: {
        parseQuestionText(text) {
            const regexp = RegExp(/\[\*.{3,10}\]/, 'g')
            const items = text.search(regexp)
            if (items == -1) return text
            else {
                let result = text
                let item = regexp.exec(text)
                while (item != null) {
                    const ident = item[0].slice(2, -1)
                    if (ident in this.previousQuestions) {
                        result = result.replace(item[0], "\"" + this.previousQuestions[ident] + "\"")
                    } else if (ident in this.previousOptions) {
                        result = result.replace(item[0], "\"" + this.previousOptions[ident] + "\"")
                    }
                    item = regexp.exec(text)
                }
                return result

            }
        },
        addAnswer() {
            this.answers.push({
                "questionnaireID": this.qID,
                "questionID": this.currentQuestion.qID,
                "session": this.session,
                "optionID": this.currentAnswer.optID,
                "opttxt": this.currentAnswer.opttxt,
                "qtext": this.currentQuestion.qtext,
                "isOpen": this.isOpenQuestion
            })

            this.previousQuestions[this.currentQuestion.qID] = this.currentQuestion.qtext
            this.previousOptions[this.currentAnswer.optID] = this.currentAnswer.opttxt

            if (this.isOpenQuestion) {
                this.nextQuestion = this.currentQuestion.options[0].nextqID
            } else {
                this.nextQuestion = this.currentAnswer.nextqID
            }
            this.currentAnswer = { "optID": null, "opttxt": null }
            if (this.nextQuestion != null) {
                axios.get("http://127.0.0.1:9103/intelliq_api/question/" + this.qID + '/' + this.nextQuestion,
                    { headers: { "X-OBSERVATORY-AUTH": "e00f8e21a864de304a6c" } }).then(
                        (response) => {
                            this.currentQuestion = response.data;
                            if (this.currentQuestion.options[0].opttxt == "<open string>") {
                                this.currentAnswer = { "optID": this.currentQuestion.options[0].optID, "opttxt": '' }
                            }
                        })
            } else {
                this.sendResponses()
                this.completed = true;
            }
        },
        async sendResponses() {
            this.currentQuestion = null
            for (let a in this.answers) {
                let ans = this.answers[a]
                if (ans.isOpen) {
                    var form = new URLSearchParams();
                    form.append("opttxt", ans.opttxt);
                } else {
                    var form = ""
                }

                axios.post(`http://127.0.0.1:9103/intelliq_api/doanswer/${ans.questionnaireID}/${ans.questionID}/${ans.session}/${ans.optionID}`,
                    form).catch((error) => {
                        console.log(error)
                    })
                await new Promise(r => setTimeout(r, 10));
            }
        }
    },
    async created() {
        //create session ID
        this.session = Math.random().toString(36).slice(2, 6)
        //get all questions
        axios.get("http://127.0.0.1:9103/intelliq_api/questionnaire/" + this.qID,
            { headers: { "X-OBSERVATORY-AUTH": "e00f8e21a864de304a6c" } }).then(
                (response) => {
                    for (let q in response.data.questions) {
                        this.questions.push(response.data.questions[q][0])

                    }
                    axios.get("http://127.0.0.1:9103/intelliq_api/question/" + this.qID + '/' + this.questions[0],
                        { headers: { "X-OBSERVATORY-AUTH": "e00f8e21a864de304a6c" } }).then(
                            (response) => {
                                this.currentQuestion = response.data;
                                if (this.currentQuestion.options[0].opttxt == "<open string>") {
                                    this.currentAnswer = { "optID": this.currentQuestion.options[0].optID, "opttxt": '' }
                                }
                            })
                })
    },
    beforeRouteLeave(to, from) {
        if (this.answers != [] && !this.completed) {
            const leave = confirm("Are you sure you want to leave?\nYour answers will be lost!")
            if (!leave) return false
            else return true
        }
    }
}
</script>