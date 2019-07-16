<template src="./nws-landing.html"></template>

<script>
  export default {
    name: 'nws-landing',
    data () {
      return {
        url: ''
      }
    },
    methods: {
      retrieveUrl () {
        this.$emit('retrieve', this.url)
      }
    }
  }
</script>

<style scoped src="./nws-landing.css"></style>
