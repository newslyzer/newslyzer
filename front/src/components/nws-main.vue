<template src="./nws-main.html"></template>

<script>
  // import * as config from '@/config'
  import nwsLoader from '@/components/nws-loader/nws-loader'
  import nwsErrorWarning from '@/components/nws-error-warning/nws-error-warning'

  import nwsHeader from '@/components/nws-header/nws-header'
  import nwsLanding from '@/components/nws-landing/nws-landing'
  import nwsAnalysisResult from '@/components/nws-analysis-result/nws-analysis-result'

  export default {
    name: 'nws-main',

    props: [ 'url', 'engine' ],

    components: {
      'nws-loader': nwsLoader,
      'nws-error-warning': nwsErrorWarning,
      'nws-landing': nwsLanding,
      'nws-header': nwsHeader,
      'nws-analysis-result': nwsAnalysisResult
    },

    data () {
      return {
        state: 'LANDING',
        article: undefined,
        error: undefined
      }
    },

    watch: {
      $route (to, from) {
        if (from.query.url && !to.query.url) {
          this.state = 'LANDING'
          this.article = undefined
          this.error = undefined
        }
      }
    },

    methods: {
      handleArticle (article) {
        if (article) {
          this.article = article.data
          this.state = 'RESULT'
          this.$router.replace({ query: { url: article.url } })
        }
      }
    }
  }
</script>

<style scoped src="./nws-main.css"></style>
