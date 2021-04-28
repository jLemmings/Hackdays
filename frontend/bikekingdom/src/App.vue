<template>
  <v-app>
    <v-app-bar
      app
      color="white"
      align-center center
    >
        <v-img
          alt="BikeKingdom Logo"
          contain

          src="https://www.bikekingdom.ch/microsites-assets/bike-kingdom/Logos/image-thumb__4113581__landingpage-logo/BikeKingdomLenzerheide_LOGO_WideBlack.webp"
          transition="scale-transition"
          height="50px"
        />

    </v-app-bar>

    <v-main>
      <Map/>
    </v-main>
  </v-app>
</template>

<script>
import Map from './components/Map';

export default {
  name: 'App',

  components: {
    Map,
  },

  data: () => ({
    //
  }),
};
</script>
