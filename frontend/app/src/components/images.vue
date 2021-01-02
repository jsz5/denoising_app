<template>
    <v-container>
        <image-menu></image-menu>
        <v-row >
            <v-col class="imageContainer">
                <v-subheader class="imageSubheader" v-if="backendImageUrl">Poglądowy obraz oryginalny</v-subheader>
                <img ref="imageSrc" />
            </v-col>
            <v-col class="imageContainer" v-if="backendImageUrl">
                <v-subheader class="imageSubheader">Obraz wynikowy</v-subheader>
                <canvas ref="canvasOutput" ></canvas>

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
      ...mapState("images", ["dialogs","backendImageUrl","imageHeight","imageWidth"]),

    },
  }


</script>

<!--<style scoped>-->
<!--div{-->
<!--    background-color: blue;-->
<!--}-->
<!--</style>-->