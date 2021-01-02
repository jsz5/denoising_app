<template>
    <v-container>
        <image-menu></image-menu>
        <v-row>
            <v-col>
                <img ref="imageSrc" alt="No Image"/>
                <v-text-field
                        value="Oryginalny obraz"
                        filled
                        readonly
                ></v-text-field>
            </v-col>
            <v-col>
                <canvas ref="canvasOutput" width="450"></canvas>
                <v-text-field
                        value="Obraz wynikowy"
                        filled
                        readonly
                ></v-text-field>
                <brightness-contrast v-if="dialogs['brightnessContrast']"></brightness-contrast>
                <hue-saturation v-if="dialogs['hueSaturation']"></hue-saturation>
            </v-col>

        </v-row>
        <upload-image></upload-image>
        <add-noise></add-noise>
        <remove-noise></remove-noise>


    </v-container>

</template>

<script>


  import UploadImage from "./uploadImage";
  import AddNoise from "./addNoise";
  import ImageMenu from "./menu";
  import BrightnessContrast from "./brightnessContrast";
  import {mapState} from "vuex";
  import HueSaturation from "./hueSaturation";
  import RemoveNoise from "./removeNoise";

  export default {
    name: "Images",
    components: {RemoveNoise, HueSaturation, BrightnessContrast, ImageMenu, AddNoise, UploadImage},
    created: function () {
      this.$store.commit("images/setImagesRef", this.$refs);
    },
    computed: {
      ...mapState("images", ["dialogs"]),

    },
  }


</script>

<style scoped>

</style>