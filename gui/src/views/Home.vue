<template>
  <div>
    <h1>Home</h1>
    <div v-for="(gps, index) in gpsData" :key="index">
      <h2>{{ gps }}</h2>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
  computed: {
    gpsData () {
      return this.$store.state.gpsData
    }
  },
  sockets: {
    connect: function () {
      console.log('Socket Connected.')
    },
    gps: function (test) {
      console.log('Data!')
    }
  }
}
</script>
