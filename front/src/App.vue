<template>
  <main class="main">
    <router-view></router-view>
  </main>
</template>

<script>
export default {
  name: 'app'
}
</script>

<style>
  @import "./styles/variables.css";

  * {
    box-sizing: border-box
  }

  body {
    background: var(--white);
    font-size: var(--medium);
    font-family: 'Roboto', sans-serif;
  }

  a {
    text-decoration: none;
    color: currentColor;
    font-weight: bold;
    border-bottom: 3px solid transparent;
    &:hover {
      border-bottom-color: currentColor;
    }
  }

  .button-more {
    text-decoration: none;
    color: var(--black);
    font-size: var(--small);
    font-weight: lighter;
    text-transform: uppercase;
    border: 1px solid var(--gray200);
    padding: 0.7rem 1rem;
    background-color: var(--gray100);
    &:hover {
      background-color: var(--gray200);
      border: 1px solid var(--gray200);
    }
  }
  table {
    border-collapse: collapse;
  }

  h2 {
    text-transform: uppercase;
    font-size: var(--xlarge);
  }

  .section {
    margin: 0 auto;
    max-width: 100rem;
    padding: 0.5rem;
  }

  .section-title {
    font-weight: bold;
    font-size: var(--large);
    & .value {
      font-size: var(--xxlarge);
    }
    & .button-more {
      float: right;
    }
  }
  .section-wrapper-light {
    background-color: var(--gray100);
  }
  .section-wrapper-dark {
    background: #3c3352;
    & h2 {
      color: var(--white);
    }
  }


  @media (--medium-viewport) {
    .section {
      padding: 1.2rem;
    }
  }

  @media (--large-viewport) {
    .section {
      padding: 2rem;
    }
    .graphs {
      display: flex;
      justify-content: space-between;

      & .graphs-block {
        width: 48%;
      }
    }
  }
</style>
