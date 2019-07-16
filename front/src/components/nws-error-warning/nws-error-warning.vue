<template src="./nws-error-warning.html"></template>

<script>
  import router from '@/router/index'
  export default {
    name: 'nws-error-warning',
    methods: {
      reload () {
        window.location.reload(true)
        router.push({ name: 'nws-index' })
      }
    }
  }
</script>

<style scoped src="./nws-error-warning.css"></style>
