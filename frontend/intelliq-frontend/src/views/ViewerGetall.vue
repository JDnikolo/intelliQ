<script>
import { RouterLink } from 'vue-router';
import { useViewerStore } from '../stores/viewerCreds.js'
import axios from 'axios';

export default {
    name: "ViewerGetall",
	setup() {
        const store = useViewerStore()
        return { store, }
    },
    data() {
        return {
            text: String,
			fullanswers: {"questionnaireID":"","full_answers":[{"questionID":"","answers":[{"session":"","ans":""}]}]},
			selected: null,
        }
    },
	props: {
		qnrID: String,
	},
    methods: {
		async getAllAnswers(id) {
			console.log("Getting All Answers")
			let token = this.store.token
            axios.get("http://127.0.0.1:9103/intelliq_api/getallanswers/" + id,
                { headers: { "X-OBSERVATORY-AUTH": token } }).then(
                    (response) => {
						this.fullanswers = response.data;

                    })
		}
    },
    async created() {
        console.log('mounting');
        this.getAllAnswers(this.qnrID);
    }
}
</script>

<template>
    <div style="background-color:#93CAED">
		<p><u>All answers of {{this.qnrID}}:</u></p>
		<table style="border: 1px solid black; border-collapse: collapse;">
			<tr><th style="border: 1px solid black;"></th>
			<th style="border: 1px solid black;" v-for="i in fullanswers.full_answers[0].answers.length">
				{{fullanswers.full_answers[0].answers[i - 1].session}}
			</th>
			</tr>
			<tr v-for="x in fullanswers.full_answers.length">
				<th style="border: 1px solid black;"> {{fullanswers.full_answers[x - 1].questionID}} </th>
				<td style="border: 1px solid black;" v-for="j in fullanswers.full_answers[x - 1].answers.length">
					{{fullanswers.full_answers[x - 1].answers[j - 1].ans}}
				</td>
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