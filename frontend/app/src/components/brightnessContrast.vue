<template>
    <v-container>
        <!--        <v-row>-->
        <!--            <img crossOrigin="anonymous" src="" id="dataimage" style=" visibility: hidden;"/>-->

        <!--        </v-row>-->
        <v-row>
            <v-subheader class="pl-0">
                Kontrast
            </v-subheader>
            <v-slider
                    v-model="contrastSlider"
                    max="5"
                    min="0"
                    step="0.01"
                    @change="changeBrightnessContrast"
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
                    @change="changeBrightnessContrast"
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
                    @click="cancelChanges"
            >
                Anuluj
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
  import {mapGetters, mapState} from "vuex";
  import {baseUrl} from "@/utils/helper";
  // import axios from "axios";
  // import axios from "axios";
  // import axios from "axios";


  export default {
    name: "brightnessContrast",


    data: () => {
      return {
        contrastSlider: 1,
        brightnessSlider: 1,
        contrastBrightnessUrl: null
      }
    },
    computed: {
      ...mapState("images", ["backendImageUrl", "showFilter"]),
      ...mapGetters("images", ["getRefs"])
    },
    // watch: {
    //   brightnessSlider() {
    //     this.changeBrightnessContrast()
    //   },
    //   contrastSlider() {
    //     this.changeBrightnessContrast()
    //   }
    // },
    methods: {
      changeBrightnessContrast() {
        console.log(baseUrl)
        // console.log(contrast_and_brightness)
        // const formData = new FormData();
        // formData.append('image_url', this.backendImageUrl)
        // formData.append("method", contrast_and_brightness)
        // formData.append('params', JSON.stringify(
        //   {
        //     "contrast": this.contrastSlider,
        //     "brightness": this.brightnessSlider
        //   }))
        // // formData.append('old_image', this.backendImageUrl)
        //
        // axios.post(baseUrl + '/images/image-processing/', formData).then(response => {
        //   console.log(response.data)
        //   this.contrastBrightnessUrl=response.data
        //   this.$store.commit('images/setCanvasOutput', baseUrl + response.data);
        //
        // })
        //   .catch(error => {
        //     console.log(error)
        //   })
        // var img = this.getRefs.canvasOutput
        // img.setAttribute('style', 'filter:brightness(' + this.brightnessSlider + ') contrast(' + this.contrastSlider + ')')
        // console.log(this.backendImageUrl)
        // var canvas = this.getRefs.canvasOutput
        // var ctx = canvas.getContext('2d');
        // ctx.filter = "brightness(" + this.brightnessSlider + ") contrast(" + this.contrastSlider + ")"
        // console.log(ctx.filter)
        // // var img = document.getElementById("dataimage");
        // // img.src = baseUrl + this.backendImageUrl
        // // img.crossOrigin = "anonymus"
        // ctx.drawImage(canvas, 0, 0);
        //
        // var img = new Image();
        // img.onload = function () {
        //   var ctx = canvas.getContext('2d');
        //   ctx.filter = "brightness(" + this.brightnessSlider + ") contrast(" + this.contrastSlider + ")"
        //   ctx.canvas.width = img.width
        //   ctx.canvas.height = img.height
        //   ctx.drawImage(img, 0, 0);
        // }
        // img.crossOrigin = "anonymous"
        // img.src = baseUrl+this.backendImageUrl

        this.$store.commit('images/setCanvasOutput', {
          "url":baseUrl + this.backendImageUrl,
          "filters":"brightness(" + this.brightnessSlider + ") contrast(" + this.contrastSlider + ")"
        });

        console.log(this.showFilter)
      },
      saveChanges() {
        this.$store.dispatch('images/saveFiltersChange')
      },
      cancelChanges(){
        this.$store.commit('images/setCanvasOutput', {
          "url":baseUrl + this.backendImageUrl
        });
        this.$store.commit('images/cancelFilter')
      }
    }
  }
</script>

<style scoped>

</style>