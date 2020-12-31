<template>
    <v-container>
        <v-row>
            <img crossOrigin="anonymous" src="" id="dataimage" style=" visibility: hidden;"/>

        </v-row>
        <v-row>
            <v-subheader class="pl-0">
                Kontrast
            </v-subheader>
            <v-slider
                    v-model="contrastSlider"
                    max="5"
                    min="0"
                    step="0.01"
                    :lazy="false"
                    :tooltip="'always'"

            >
                <template v-slot:append>
                    <v-text-field
                            v-model="contrastSlider"
                            class="mt-0 pt-0"
                            hide-details
                            single-line
                            style="width: 60px"
                    ></v-text-field>
                </template>
            </v-slider>
        </v-row>
        <v-row>
            <v-subheader class="pl-0">
                Jasność
            </v-subheader>
            <v-slider
                    v-model="brightnessSlider"
                    max="5"
                    min="0"
                    step="0.01"
                    :lazy="false"
            >

                <template v-slot:append>
                    <v-text-field
                            v-model="brightnessSlider"
                            class="mt-0 pt-0"
                            hide-details
                            single-line
                            style="width: 60px"
                    ></v-text-field>
                </template>
            </v-slider>
        </v-row>
        <v-row>
            <v-spacer></v-spacer>
            <v-btn
                    color="green darken-1"
                    text
                    @click="saveChanges"
            >
                Ok
            </v-btn>
            <v-btn
                    text
                    @click="$store.commit('images/cancelFilter')"
            >
                Anuluj
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
  import {mapGetters, mapState} from "vuex";
  import {baseUrl} from "../utils/helper";
  // import axios from "axios";
  // import axios from "axios";


  export default {
    name: "brightnessContrast",


    data: () => {
      return {
        contrastSlider: 1,
        brightnessSlider: 1,
      }
    },
    computed: {
      ...mapState("images", ["backendImageUrl"]),
      ...mapGetters("images", ["getRefs"])
    },
    watch: {
      brightnessSlider() {
        this.changeBrightnessContrast()
      },
      contrastSlider() {
        this.changeBrightnessContrast()
      }
    },
    methods: {
      changeBrightnessContrast() {
        var img = this.getRefs.canvasOutput
        img.setAttribute('style', 'filter:brightness(' + this.brightnessSlider + ') contrast(' + this.contrastSlider + ')')

      },
      saveChanges() {
        var canvas = this.getRefs.canvasOutput
        var ctx = canvas.getContext('2d');
        ctx.filter = "brightness(" + '500%' + ") contrast(" + this.contrastSlider + ")"
        console.log(ctx.filter)
        var img = document.getElementById("dataimage");
        img.src = baseUrl + this.backendImageUrl
        img.crossOrigin = "anonymus"
        ctx.drawImage(img, 0, 0);

        this.$store.dispatch('images/saveFiltersChange', canvas.toDataURL('image/png'))
      }
    }
  }
</script>

<style scoped>

</style>