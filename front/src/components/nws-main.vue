<template>
  <div>
    <transition name="loading">
      <nws-loader v-if="loading"></nws-loader>
    </transition>

    <transition name="pop">
      <nws-error-warning v-if="error"></nws-error-warning>
    </transition>

    <nws-header></nws-header>

    <nws-landing v-if="!article.metadata" @retrieve="updateUrlAndRetrieve"></nws-landing>
    <nws-hero v-if="article.metadata" :metadata="article.metadata"></nws-hero>

    <nws-sentiments v-if="article.sentences" :article="article"></nws-sentiments>

    <div class="section-wrapper-light">
      <nws-words v-if="article.metadata" :article="article"></nws-words>
    </div>
    <div class="section graphs" v-if="article.sentences">
      <div class="graphs-block">
        <h2>Sentences</h2>
        <nws-sentiment-evolution
          :sentences="article.sentences">
        </nws-sentiment-evolution>
      </div>
      <div class="graphs-block" v-if="article.other">
        <h2>Words</h2>
        <nws-word-cloud
          :article="article">
        </nws-word-cloud>
      </div>
    </div>
    <nws-particles
      v-if="article.people"
      id="people-particles"
      :type="'people'"
      :particles="article.people">
    </nws-particles>
    <nws-particles
      v-if="article.places"
      id="places-particles"
      :type="'places'"
      :particles="article.places">
    </nws-particles>
    <nws-particles
      v-if="article.organizations"
      id="organizations-particles"
      :type="'organizations'"
      :particles="article.organizations">
    </nws-particles>
  </div>
</template>

<script>
import nwsLoader from './nws-loader/nws-loader'
import nwsHeader from '@/components/nws-header/nws-header'
import nwsHero from './nws-hero/nws-hero'
import nwsSentiments from './nws-sentiments/nws-sentiments'
import nwsWords from './nws-words/nws-words'
import nwsParticles from './nws-particles/nws-particles'
import nwsSentimentEvolution from './nws-sentiment-evolution/nws-sentiment-evolution'
import nwsWordCloud from './nws-word-cloud/nws-word-cloud'
import nwsLanding from './nws-landing/nws-landing'
import nwsErrorWarning from './nws-error-warning/nws-error-warning'

export default {
  name: 'nws-main',
  components: {
    'nws-loader': nwsLoader,
    'nws-hero': nwsHero,
    'nws-sentiments': nwsSentiments,
    'nws-words': nwsWords,
    'nws-particles': nwsParticles,
    'nws-sentiment-evolution': nwsSentimentEvolution,
    'nws-word-cloud': nwsWordCloud,
    'nws-landing': nwsLanding,
    'nws-header': nwsHeader,
    'nws-error-warning': nwsErrorWarning
  },
  data () {
    return {
      article: {},
      loading: true,
      error: false
    }
  },
  props: ['url', 'engine'],
  mounted: function () {
    if (this.url) {
      this.retrieveArticle()
    } else {
      this.loading = false
    }
  },
  methods: {
    retrieveArticle (newUrl) {
      var url
      if (newUrl) {
        url = newUrl
      } else {
        url = this.url
      }
      this.$router.replace({ query: { url: url } })
      this.$http.get('http://localhost:5000/article?url=' + url + '&engine=' + this.engine)
      .then(response => {
        this.loading = false
        this.article = response.body
      }, response => {
        this.error = true
      })
    },
    updateUrlAndRetrieve (value) {
      this.loading = true
      this.retrieveArticle(value)
    }
  }
}
</script>

<style>
.loading-leave-active {
  opacity: 1;
  transition: opacity 1s cubic-bezier(0.215, 0.610, 0.355, 1);
}
.loading-leave-to {
  opacity: 0;
}

.pop-enter-active,
.pop-leave-active {
  animation: slide-in-blurred-right 0.3s cubic-bezier(0.230, 1.000, 0.320, 1.000) both;
}

.pop-leave-active {
  animation-direction: reverse;
}

.pop-enter-to,
.pop-leave-to {
  transform: translateX(-5vw);
  opacity: 1;
}

@keyframes slide-in-blurred-right {
  0% {
    transform: translateX(10vw) scaleX(2.5) scaleY(0.2);
    transform-origin: 0% 50%;
    filter: blur(40px);
    opacity: 0;
  }
  100% {
    transform: translateX(1vw) scaleY(1) scaleX(1);
    transform-origin: 50% 50%;
    filter: blur(0);
    opacity: 1;
  }
}

</style>
