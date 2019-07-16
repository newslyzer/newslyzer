<template src="./nws-particle-graph.html"></template>

<script>
  export default {
    name: 'nws-particle-graph',
    props: ['context'],
    computed: {
      negative: function () {
        return this.context.filter(this.isNegative).length
      },
      neutral: function () {
        return this.context.filter(this.isNeutral).length
      },
      positive: function () {
        return this.context.filter(this.isPositive).length
      }
    },
    methods: {
      isNegative (value) {
        return value.sentiment <= -0.2
      },
      isNeutral (value) {
        return value.sentiment > -0.2 && value.sentiment < 0.2
      },
      isPositive (value) {
        return value.sentiment >= 0.2
      },
      getPercent (value) {
        return (value / this.context.length).toLocaleString('en', {style: 'percent', maximumFractionDigits: 2})
      }
    }
  }
</script>

<style scoped src="./nws-particle-graph.css"></style>
