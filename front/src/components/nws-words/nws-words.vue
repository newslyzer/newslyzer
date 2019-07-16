<template src="./nws-words.html"></template>

<script>
  import nwsParticleGraph from '../nws-particle-graph/nws-particle-graph'
  export default {
    name: 'nws-words',
    props: ['article'],
    components: {
      'nws-particle-graph': nwsParticleGraph
    }
  }
</script>

<style scoped src="./nws-words.css"></style>
