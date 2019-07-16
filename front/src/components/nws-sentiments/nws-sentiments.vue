<template src="./nws-sentiments.html"></template>

<script>
  import nwsSentimentsGraph from '../nws-sentiments-graph/nws-sentiments-graph'
  export default {
    name: 'nws-sentiments',
    props: ['article'],
    computed: {
      entities: function () {
        const words = []
        const people = this.article.people
        const places = this.article.places
        const organizations = this.article.organizations
        return words.concat(people, places, organizations)
      }
    },
    components: {
      'nws-sentiments-graph': nwsSentimentsGraph
    },
    methods: {
      mergeEntities () {
        this.$http.get('http://localhost:5000/article?url=' + this.url)
        .then(response => {
          this.article = response.body
        })
      }
    }
  }
</script>

<style scoped src="./nws-sentiments.css"></style>
