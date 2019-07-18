<template src="./nws-analysis-result.html"></template>

<script>
  import * as config from '@/config'
  import nwsHero from '@/components/nws-hero/nws-hero'
  import nwsSentiments from '@/components/nws-sentiments/nws-sentiments'
  import nwsWords from '@/components/nws-words/nws-words'
  import nwsParticles from '@/components/nws-particles/nws-particles'
  import nwsSentimentEvolution from '@/components/nws-sentiment-evolution/nws-sentiment-evolution'
  import nwsWordCloud from '@/components/nws-word-cloud/nws-word-cloud'

  export default {
    name: 'nws-analysis-result',
    props: [ 'article' ],

    components: {
      'nws-hero': nwsHero,
      'nws-sentiments': nwsSentiments,
      'nws-words': nwsWords,
      'nws-particles': nwsParticles,
      'nws-sentiment-evolution': nwsSentimentEvolution,
      'nws-word-cloud': nwsWordCloud
    },

    methods: {
      wordcloudImage () {
        return `${config.wordcloudBase}/${this.article.wordcloud}`
      }
    }
  }
</script>

<style scoped src="./nws-analysis-result.css"></style>
