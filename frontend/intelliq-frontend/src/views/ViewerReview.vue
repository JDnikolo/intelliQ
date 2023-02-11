<script>
import { RouterLink } from 'vue-router';
import { useViewerStore } from '../stores/viewerCreds.js'
import axios from 'axios';

export default {
    name: "ViewerReview",
	setup() {
        const store = useViewerStore()
        return { store, }
    },
    data() {
        return {
            text: String,
			questionsinfo: {},
			selected: null,
        }
    },
	props: {
		qnrID: String,
	},
    methods: {
		async review(id) {
			console.log("Reviewing")
			let token = this.store.token
            axios.get("http://127.0.0.1:9103/getQuestionsInfo/" + id,
                { headers: { "X-OBSERVATORY-AUTH": token } }).then(
                    (response) => {
						this.questionsinfo = response.data;

                    })
		}
    },
    async created() {
        console.log('mounting');
        this.review(this.qnrID);
    }
}
</script>

<template>
	<p><i>Details about {{this.qnrID}}</i></p>
	<div style="background-color:#93CAED">
		<table style="border: 1px solid black; border-collapse: collapse;">
			<th style="border: 1px solid black;"> QuestionID </th>
			<th style="border: 1px solid black;"> Question Text </th>
			<th style="border: 1px solid black;"> Required </th>
			<th style="border: 1px solid black;"> Type </th>
			<th style="border: 1px solid black;"> OptionID </th>
			<th style="border: 1px solid black;"> Option Text </th>
			<th style="border: 1px solid black;" >Next Question </th>
			<tr v-for="x in questionsinfo.length">
				<th style="border: 1px solid black;"> {{questionsinfo[x - 1][0]}} </th>
				<td style="border: 1px solid black;"> {{questionsinfo[x - 1][1]}} </td>
				<td style="border: 1px solid black;" v-if="questionsinfo[x - 1][2] === 1"> Yes </td>
				<td style="border: 1px solid black;" v-else> No </td>
				<td style="border: 1px solid black;"> {{questionsinfo[x - 1][3]}} </td>
				<td style="border: 1px solid black;"> {{questionsinfo[x - 1][4]}} </td>
				<td style="border: 1px solid black;"> {{questionsinfo[x - 1][5]}} </td>
				<td style="border: 1px solid black;"> {{questionsinfo[x - 1][6]}} </td>
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