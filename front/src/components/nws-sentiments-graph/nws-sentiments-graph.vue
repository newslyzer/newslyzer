<template src="./nws-sentiments-graph.html"></template>

<script>
  export default {
    name: 'nws-sentiments-graph',
    props: [
      'type',
      'data'
    ],
    computed: {
      negative: function () {
        return this.data.filter(this.isNegative)
      },
      neutral: function () {
        return this.data.filter(this.isNeutral)
      },
      positive: function () {
        return this.data.filter(this.isPositive)
      }
    },
    methods: {
      isNegative (value) {
        return value.sentiment < -0.2
      },
      isNeutral (value) {
        return value.sentiment > -0.2 && value.sentiment < 0.2
      },
      isPositive (value) {
        return value.sentiment > 0.2
      },
      getPercent (value) {
        return (value / this.data.length).toLocaleString('en', {style: 'percent', maximumFractionDigits: 2})
      }
    }
  }
</script>

<style scoped src="./nws-sentiments-graph.css"></style>
