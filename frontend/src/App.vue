<template>
<b-container fluid id="app">
  <SiteHeader/>
  <b-row id="main-pane">
    <b-col sm="4">
      <info-form/>
    </b-col>
    <b-col sm="8">
      <ref-tables/>
    </b-col>
  </b-row>
</b-container>
</template>

<script>
import SiteHeader from './components/SiteHeader'
import InfoForm from './components/InfoForm'
import RefTables from './components/RefTables'

export default {
  name: 'app',
  components: {
    SiteHeader, InfoForm, RefTables
  }
}
</script>

<style>
body {
  padding: 0;
  margin: 0;
}

#app {
  padding: 0;
  margin: 0;
}

h1, h2, h3, h4, h5, h6, p {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

footer {
  background-color: #555;
  color: white;
  padding: 15px;
}
</style>
