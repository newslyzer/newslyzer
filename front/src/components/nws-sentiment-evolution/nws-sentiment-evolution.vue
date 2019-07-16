<template>
  <div>
    <line-chart
      :chart-data="datacollection"
      :options="options"
      :height="200">
    </line-chart>

    <div class="feeling" title="Range is in -1 y 1">
      <span class="feeling-txt">
        <template v-if="sentiment < -0.6">VERY NEGATIVE</template>
        <template v-else-if="sentiment > -1 && sentiment <= -0.6">VERY NEGATIVE</template>
        <template v-else-if="sentiment > -0.6 && sentiment <= -0.2">NEGATIVE</template>
        <template v-else-if="sentiment > -0.2 && sentiment <= 0.2">NEUTRAL</template>
        <template v-else-if="sentiment > 0.2 && sentiment <= 0.6">POSITIVE</template>
        <template v-else-if="sentiment > 0.6 && sentiment <= 1">VERY POSITIVE</template>
      </span>
      <span v-if="twoDecSent" class="feeling-num">{{ twoDecSent }}</span>
      <span :class="feeling" class="feeling-bar"></span>
    </div>

    <p> {{ context }} </p>
  </div>
</template>

<script>
import LineChart from './line-chart.js'

export default {
  components: {
    LineChart
  },
  props: ['sentences'],
  data () {
    return {
      datacollection: null,
      options: null,
      context: '',
      texts: [],
      sentiment: 100,
      twoDecSent: null,
      feeling: ''
    }
  },
  mounted () {
    this.fillData()
  },
  methods: {
    setTitle (tooltipItem) {
      this.context = this.texts[tooltipItem.index]
      this.sentiment = tooltipItem.yLabel
      if (this.sentiment) {
        this.twoDecSent = this.sentiment.toLocaleString('en', {maximumFractionDigits: 2})
      }

      if (this.sentiment < -0.6) {
        this.feeling = 'v-negative'
      } else if (this.sentiment > -0.6 && this.sentiment <= -0.2) {
        this.feeling = 'negative'
      } else if (this.sentiment > -0.2 && this.sentiment <= 0.2) {
        this.feeling = 'neutral'
      } else if (this.sentiment > 0.2 && this.sentiment <= 0.6) {
        this.feeling = 'positive'
      } else {
        this.feeling = 'v-positive'
      }

      return tooltipItem.yLabel
    },
    fillData () {
      // Overwriting base render method with actual data.
      var lastSentiment = null
      const positiveSentiments = []
      const negativeSentiments = []
      const labels = []
      this.texts = []
      for (const sentence of this.sentences) {
        const sentiment = sentence.sentiment
        const text = sentence.text
        if (lastSentiment && ((lastSentiment < 0 && sentiment > 0) || (lastSentiment > 0 && sentiment < 0))) {
          negativeSentiments.push(0)
          positiveSentiments.push(0)
          labels.push('')
          this.texts.push('')
        }

        if (sentiment > 0) {
          positiveSentiments.push(sentiment)
          negativeSentiments.push(null)
        } else if (sentiment < 0) {
          positiveSentiments.push(null)
          negativeSentiments.push(sentiment)
        } else {
          positiveSentiments.push(0)
          negativeSentiments.push(0)
        }
        lastSentiment = sentiment
        this.texts.push(text)
        labels.push('')
      }

      this.datacollection = {
        labels: labels,
        datasets: [
          {
            backgroundColor: '#1DCD9F',
            data: positiveSentiments
          },
          {
            backgroundColor: '#EE5A5A',
            data: negativeSentiments
          }
        ]
      }

      this.options = {
        scales: {
          yAxes: [{
            ticks: {
              min: -1,
              max: 1
            }
          }]
        },
        legend: {
          display: false
        },
        tooltips: {
          callbacks: {
            label: this.setTitle
          }
        }
      }
    }
  }
}
</script>

<style scoped src="./nws-sentiment-evolution.css"></style>
