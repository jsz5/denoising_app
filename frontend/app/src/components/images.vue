<template>
    <v-container>
        <image-menu></image-menu>
        <v-row>
            <v-col>
                <img ref="imageSrc" alt="No Image"/>
            </v-col>
            <v-col>
                <canvas ref="canvasOutput" width="450"></canvas>
                <brightness-contrast v-if="showFilter==='brightnessContrast'"></brightness-contrast>
                <hue-saturation  v-if="showFilter==='hueSaturation'"></hue-saturation>
            </v-col>

        </v-row>
        <upload-image></upload-image>
        <add-noise></add-noise>


    </v-container>

</template>

<script>


  import UploadImage from "./uploadImage";
  import AddNoise from "./addNoise";
  import ImageMenu from "./menu";
  import BrightnessContrast from "./brightnessContrast";
  import {mapState} from "vuex";
  import HueSaturation from "./hueSaturation";

  export default {
    name: "Images",
    components: {HueSaturation, BrightnessContrast, ImageMenu, AddNoise, UploadImage},
    created: function () {
      this.$store.commit("images/setImagesRef", this.$refs);
    },
    computed: {
      ...mapState("images", ["showFilter"]),

    },
  }


</script>

<style scoped>

</style>