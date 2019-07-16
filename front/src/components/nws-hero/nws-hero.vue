<template src="./nws-hero.html"></template>

<script>
  export default {
    name: 'nws-hero',
    props: ['metadata'],
    computed: {
      twoDecSent: function () {
        return this.metadata.sentiment.toLocaleString('en', {maximumFractionDigits: 2})
      },
      feeling: function () {
        if (this.metadata.sentiment < -0.6) {
          return 'v-negative'
        } else if (this.metadata.sentiment > -0.6 && this.metadata.sentiment <= -0.2) {
          return 'negative'
        } else if (this.metadata.sentiment > -0.2 && this.metadata.sentiment <= 0.2) {
          return 'neutral'
        } else if (this.metadata.sentiment > 0.2 && this.metadata.sentiment <= 0.6) {
          return 'positive'
        } else {
          return 'v-positive'
        }
      },
      viralize: function () {
        const string = `I have analyzed the sentiment of '${this.metadata.title}' by '${this.metadata.sourceName}'`
        return encodeURI(string)
      }
    }
  }
</script>

<style scoped src="./nws-hero.css"></style>
