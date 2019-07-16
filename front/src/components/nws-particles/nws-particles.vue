<template src="./nws-particles.html"></template>

<script>
  import nwsParticleSingle from '../nws-particle-single/nws-particle-single'
  export default {
    name: 'nws-particles',
    props: [
      'particles',
      'type'
    ],
    components: {
      'nws-particle-single': nwsParticleSingle
    }
  }
</script>

<style scoped src="./nws-particles.css"></style>
