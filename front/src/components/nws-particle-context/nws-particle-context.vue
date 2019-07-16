<template src="./nws-particle-context.html"></template>

<script>
  import nwsParticleContextSingle from '../nws-particle-context-single/nws-particle-context-single'
  export default {
    name: 'nws-particle-context',
    props: [
      'word',
      'context'
    ],
    components: {
      'nws-particle-context-single': nwsParticleContextSingle
    },
    computed: {
      positives: function () {
        return this.context.filter((context) => context.sentiment > 0.2)
      },
      neutrals: function () {
        return this.context.filter((context) => context.sentiment > -0.2 && context.sentiment < 0.2)
      },
      negatives: function () {
        return this.context.filter((context) => context.sentiment < -0.2)
      }
    },
    methods: {
      getPercent (partLength) {
        return (partLength / this.context.length).toLocaleString('en', {style: 'percent', maximumFractionDigits: 2})
      }
    }
  }
</script>

<style scoped src="./nws-particle-context.css"></style>
