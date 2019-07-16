<template src="./nws-particle-context-single.html"></template>

<script>
  export default {
    name: 'nws-particle-context-single',
    props: [
      'word',
      'sentence'
    ],
    computed: {
      markedSentence: function () {
        return this.sentence.sentence.replace(new RegExp(this.word, 'gi'), `<span class="mark ${this.sentiment}">${this.word}</span>`)
      },
      sentiment: function () {
        if (this.sentence.sentiment < -0.2) {
          return 'negative'
        } else if (this.sentence.sentiment >= -0.2 && this.sentence.sentiment <= 0.2) {
          return 'neutral'
        } else if (this.sentence.sentiment > 0.2) {
          return 'positive'
        }
      }
    }
  }
</script>

<style src="./nws-particle-context-single.css"></style>
