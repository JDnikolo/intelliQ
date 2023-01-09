<template><div>
        Log in before continuing:
        <div v-if="message != ''">
            {{ message }}
        </div>
        <div>
            <div>
                <label>Username: </label>
                <input type="text" v-model="username">
            </div>
            <div>
                <label>Password: </label>
                <input type="password" v-model="password">
            </div>
            <button @click="tryLogin()">Log in</button>
        </div>
        <div>{{ username }} {{ password }} {{ token }}</div>
    </div>

</template>
<script>
import axios from 'axios'
import { useAdminStore } from '../stores/adminCreds.js'
export default {
    name: "AdminLogin",
    setup() {
        const store = useAdminStore()
        return { store, }
    },
    data() {
        return {
            password: '',
            username: '',
            message: '',
            token: '',
        }
    },
    methods: {
        tryLogin() { <!-- MUST CHECK THIS IS ACTUALLY ADMIN AND NOT USER -->
			<!-- Perhaps admin credentials should also be saved in viewer store -->
            let admin = this.username, pass = this.password
            var form = new URLSearchParams();
            form.append("username", admin);
            form.append("password", pass);
            <!--console.log(form)-->
			const options = {
				headers: {"content-type": "application/x-www-form-urlencoded"}
			}
            axios.post("http://127.0.0.1:9103/intelliq_api/login", form, options).then((response) => {
                this.token = response.data.token
                console.log(this.token)
                this.message = "Login Successful, redirecting..."
                this.store.setBoth(admin, this.token)
                this.redirect()
            }).catch((error) => {
                console.log(error)
                if (error.status == 400) {
                    this.message = "Incorrect Credentials"
                }
            })
        },
        async redirect() {
            await new Promise(r => setTimeout(r, 1000));
            this.$router.replace("/admin/endpoints")
        }
    },
    created() {
		if (this.store.token != null) {
            this.$router.replace("/admin/endpoints")
        }
    }
}
</script>