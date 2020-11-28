<template>
    <v-container>
        <image-menu></image-menu>
        <v-row>
            <v-col>
                <img ref="imageSrc" alt="No Image"/>
            </v-col>
            <v-col>
                <canvas ref="canvasOutput"></canvas>
                <div class="caption">canvasOutput</div>
                <brightness-contrast></brightness-contrast>
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
  export default {
    name: "Images",
    components: {BrightnessContrast, ImageMenu, AddNoise, UploadImage},
    created: function () {
      this.$store.commit("images/setImagesRef", this.$refs);
    }
  }


</script>

<style scoped>

</style>