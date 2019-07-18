<template src="./nws-analyze-input.html"></template>

<script>
  import * as config from '@/config'
  export default {
    name: 'nws-analyze-input',

    props: [ 'position', 'currentUrl' ],

    data () {
      return {
        url: undefined,
        progress: undefined
      }
    },

    mounted () {
      if (this.currentUrl) {
        this.url = this.currentUrl
        this.retrieveUrl()
      }
    },

    watch: {
      currentUrl (val, oldVal) {
        if (typeof val !== 'undefined') {
          this.url = this.currentUrl
          this.retrieveUrl()
        } if (val === this.url) {
          this.url = undefined
        }
      }
    },

    methods: {
      validateUrl () {
        return !!this.url
      },

      subscribeNotifications (data) {
        var source = new EventSource(data.notifications)

        source.onmessage = (event) => {
          const data = JSON.parse(event.data)

          if (data.status === 'in_progress') {
            this.progress = parseInt(data.progress, 10)
          } else {
            source.close()
            this.retrieveUrl()
          }
        }
      },

      retrieveUrl () {
        // this.$emit('retrieve', this.url)
        const url = this.url

        this.progress = 0

        const apiPath = `${config.baseApi}/article?url=${url}`

        this.$http.get(apiPath).then(response => {
          const data = response.body

          if (data.status === 'in_progress') {
            this.subscribeNotifications(data)
          } else {
            this.progress = undefined
            this.url = undefined
            this.$emit('article', { url, data })
          }
        }, error => {
          this.progress = undefined
          this.$emit('error', error)
        })
      }
    }
  }
</script>

<style scoped src="./nws-analyze-input.css"></style>
