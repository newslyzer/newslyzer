<template src="./nws-particle-single.html"></template>

<script>
  import nwsParticleContext from '../nws-particle-context/nws-particle-context'
  export default {
    name: 'nws-particle-single',
    data () {
      return {
        extend: false
      }
    },
    props: [
      'particle'
    ],
    components: {
      'nws-particle-context': nwsParticleContext
    },
    computed: {
      sentiment: function () {
        if (this.particle.sentiment < -0.6) {
          return 'v-negative'
        } else if (this.particle.sentiment < -0.2) {
          return 'negative'
        } else if (this.particle.sentiment < 0.2) {
          return 'neutral'
        } else if (this.particle.sentiment < 0.6) {
          return 'positive'
        } else {
          return 'v-positive'
        }
      },
      barLength: function () {
        if (Math.sign(this.particle.sentiment) === '-1') {
          return -Math.abs(this.particle.sentiment) * 100
        } else {
          return Math.abs(this.particle.sentiment) * 100
        }
      }
    },
    methods: {
      extendParticle () {
        this.extend = !this.extend
      }
    }
  }
</script>

<style scoped src="./nws-particle-single.css"></style>
