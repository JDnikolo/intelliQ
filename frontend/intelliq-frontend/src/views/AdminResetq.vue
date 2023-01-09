<script>
import { RouterLink } from 'vue-router';
import { useAdminStore } from '../stores/adminCreds.js'
import axios from 'axios';

export default {
    name: "AdminResetq",
	setup() {
        const store = useAdminStore()
        return { store, }
    },
    data() {
        return {
            status: {},
			sanswers: {"answers":
        {
            "qID": "",
            "ans": ""
        }},
			selected: null,
        }
    },
	props: {
		qnrID: String,
	},
    methods: {
		async resetq(id) {
            console.log("Reseting questionnaire")
			let token = this.store.token
			console.log(token)
			//const options = { headers: {"content-type": "application/x-www-form-urlencoded"} }
            axios.post("http://127.0.0.1:9103/intelliq_api/admin/resetq/" + id, '',
                { headers: { "X-OBSERVATORY-AUTH": token } }).then(
                    (response) => {
                        this.status = response.data;

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
    async created() {
        console.log('mounting');
        this.resetq(this.qnrID);
    }
}
</script>
<template>
    <div style="background-color:#F47174">
		<p>{{this.status}}</p>
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