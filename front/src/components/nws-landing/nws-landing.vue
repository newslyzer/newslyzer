<template src="./nws-landing.html"></template>

<script>
  import nwsAnalyzeInput from '@/components/nws-analyze-input/nws-analyze-input'

  export default {
    name: 'nws-landing',

    props: [ 'progress', 'currentUrl' ],

    components: {
      'nws-analyze-input': nwsAnalyzeInput
    },

    methods: {
      handleArticle (article) {
        this.$emit('article', article)
      }
    }
  }
</script>

<style scoped src="./nws-landing.css"></style>
