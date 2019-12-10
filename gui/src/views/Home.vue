<template>
  <div>
    <h1>Home</h1>
    <div v-for="(gps, index) in gps_data" :key="index">
      <h2>{{ gps }}</h2>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
  data () {
    return {
      gps_data: []
    }
  },
  sockets: {
    connect: function () {
      console.log('Socket Connected.')
    },
    gps_data: function (test) {
      console.log(test)
      this.gps_data.push(test)
    }
  }
}
</script>
