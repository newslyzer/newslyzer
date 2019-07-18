<template src="./nws-main.html"></template>

<script>
  import * as config from '@/config'
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
        loading: false,
        error: undefined,
        progress: 0
      }
    },

    watch: {
      $route (to, from) {
        if (from.query.url && !to.query.url) {
          this.state = 'LANDING'
          this.article = undefined
          this.loading = false
          this.error = undefined
          this.progress = 0
        }
      }
    },

    mounted: function () {
      if (this.url) {
        this.retrieveArticle()
      } else {
        this.loading = false
      }
    },

    methods: {
      retrieveArticle (newUrl) {
        const url = newUrl || this.url

        const apiPath = `${config.baseApi}/article?url=${url}&engine=${this.engine}`

        this.$router.replace({ query: { url: url } })
        this.$http.get(apiPath).then(response => {
          const data = response.body

          if (data.status === 'in_progress') {
            // Subscribe to the notifications
            this.state = 'PROCESSING'
            var source = new EventSource(data.notifications)

            source.onmessage = (event) => {
              console.log('event', event)
              const data = JSON.parse(event.data)
              if (data.status === 'in_progress') {
                this.progress = parseInt(data.progress, 10)
              } else {
                this.retrieveArticle(this.url)
              }
            }
          } else {
            // Load the results
            this.loading = false
            this.state = 'RESULT'
            this.article = data
          }

          // this.loading = false
          // this.article = response.body
        }, error => {
          this.error = error
        })
      },
      updateUrlAndRetrieve (value) {
        this.loading = true
        this.retrieveArticle(value)
      }
    }
  }
</script>

<style scoped src="./nws-main.css"></style>
