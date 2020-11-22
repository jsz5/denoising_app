<template>
    <v-app>
        <Menu></Menu>
        <v-main>
            <Images></Images>
        </v-main>
    </v-app>
</template>

<script>
  import Menu from '@/components/Menu';
  import Images from '@/components/Images';

  export default {
    name: 'App',

    components: {
      Menu,
      Images
    },

    data: () => ({
      //
    }),
  };
</script>
