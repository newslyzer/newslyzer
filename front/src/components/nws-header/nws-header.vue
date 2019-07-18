<template src="./nws-header.html"></template>

<script>
  import nwsAnalyzeInput from '@/components/nws-analyze-input/nws-analyze-input'

  export default {
    name: 'nws-header',

    props: [ 'showSearch', 'currentUrl' ],

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

<style scoped src="./nws-header.css"></style>
