<template src="./nws-word-cloud.html"></template>

<script>
import VueWordCloud from 'vuewordcloud'

export default {
  components: {
    [VueWordCloud.name]: VueWordCloud
  },
  props: ['article'],
  data () {
    return {
      words: [],
      processedColors: {}
    }
  },
  created: function () {
    const words = [...this.article.organizations, ...this.article.places, ...this.article.people]
    for (const word of words) {
      this.words.push([word.name, word.frequency])
      if (word.sentiment < -0.6) {
        this.processedColors[word.name] = 'rgb(238, 90, 90)'
      } else if (word.sentiment < -0.2) {
        this.processedColors[word.name] = 'rgb(255, 177, 116)'
      } else if (word.sentiment < 0.2) {
        this.processedColors[word.name] = 'rgb(252, 227, 138)'
      } else if (word.sentiment < 0.6) {
        this.processedColors[word.name] = 'rgb(143, 236, 200)'
      } else {
        this.processedColors[word.name] = 'rgb(29, 205, 159)'
      }
    }
  },
  computed: {
    colors: function () {
      const processedColors = this.processedColors
      function calculateColor ([word]) {
        return processedColors[word]
      }
      return (calculateColor)
    }
  }
}
</script>

<style scoped src="./nws-word-cloud.css"></style>
