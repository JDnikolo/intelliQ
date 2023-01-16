<template>\<div>
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
                <input type="password" v-model="password" v-on:keyup.enter="tryLogin()">
            </div>
            <button @click="tryLogin()">Log in</button>
        </div>
    </div>

</template>
<script>
import axios from 'axios'
import { useViewerStore } from '../stores/viewerCreds.js'
export default {
    name: "ViewerLogin",
    setup() {
        const store = useViewerStore()
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
        tryLogin() {
            let user = this.username, pass = this.password
            var form = new URLSearchParams();
            form.append("username", user);
            form.append("password", pass);
            axios.post("http://127.0.0.1:9103/intelliq_api/login", form).then((response) => {
                this.token = response.data.token
                console.log(this.token)
                this.message = "Login Successful, redirecting..."
                this.store.setBoth(user, this.token)
                this.redirect()
            }).catch((error) => {
                console.log(error)
                if (error.response.status == 401) {
                    this.message = "Incorrect credentials!"
                }
            })
        },
        async redirect() {
            await new Promise(r => setTimeout(r, 1000));
            this.$router.replace("viewer/endpoints")
        }
    },
    created() {
        if (this.store.token != null) {
            this.$router.replace("/viewer/endpoints")
        }
    }
}
</script>