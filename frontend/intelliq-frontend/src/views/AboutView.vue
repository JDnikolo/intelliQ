<template>
  <div class="about">
    <h1>Testing: accessing the api</h1>
  </div>
  <div>{{ something }}</div>
  <div v-for="q in questions">{{ q }}</div>
</template>
<script>
import axios from 'axios'
export default {
  data() {
    return {
      questions: [1, 2, 3],
      something: null,
    }
  },
  created() {
    axios.get("http://localhost:5000/questionnaire/QQ000",
      { headers: { "X-OBSERVATORY-AUTH": "e00f8e21a864de304a6c" } }).then(
        (response) => {
          console.log(response.data);
          this.something = response.data.questionnaireID[0];
          this.questions = response.data.questions
        });
  }
}
</script>
<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
