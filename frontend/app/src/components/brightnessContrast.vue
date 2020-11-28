<template>
    <v-container>
        <v-row justify="center">
            <v-dialog
                    v-model="brightnessContrastDialog"

            >
                <v-card>
                    <v-card-title>
                        Zmień kontrast i jasność
                    </v-card-title>
                    <v-card-text>
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
                                    @change="changeContrastBrightness"

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
                            <!--                            <input type="range" id="trackbar" value="50" min="0" max="100" step="1" oninput="changeContrastBrightness()">-->
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
                        <div>
                            <v-img
                                    :src="initialImage"
                            ></v-img>
                            <canvas id="canvasBrightnessContrast" ref="canvasBrightnessContrast"></canvas>
                        </div>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                                color="green darken-1"
                                text
                                @click="$store.dispatch('images/newImage',sourceImage)"
                        >
                            Ok
                        </v-btn>
                        <v-btn
                                text
                                @click="$store.commit('images/cancelBrightnessContrastDialog')"
                        >
                            Anuluj
                        </v-btn>

                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </v-container>
</template>

<script>
  import {mapGetters, mapState} from "vuex";


  export default {
    name: "brightnessContrast",


    data: () => {
      return {
        contrastSlider: 1,
        brightnessSlider: 1,
        mat: null,
        initialImage: null,
        tmp: null
      }
    },
    computed: {
      ...mapState("images", ["brightnessContrastDialog", "resultMat"]),
      ...mapGetters("images", ["getRefs"])

    },
    watch: {
      brightnessSlider() {
        var img = document.getElementById('canvasBrightnessContrast');
        img.setAttribute('style', 'filter:brightness(' + this.brightnessSlider + '); -webkit-filter:brightness(' + this.brightnessSlider + '); -moz-filter:brightness(' + this.brightnessSlider + ')');
      },
      contrastSlider(){
        var img = document.getElementById('canvasBrightnessContrast');
        img.setAttribute('style', 'filter:contrast(' + this.contrastSlider + '); -webkit-filter:contrast(' + this.contrastSlider + '); -moz-filter:contrast(' + this.contrastSlider + ')');

      }
    },
    methods: {
      sourceImage() {
        let src
        if (this.resultMat == null) {
          src = this.$cv2.imread(this.getRefs.imageSrc)
        } else {
          let output = this.$cv2.imread(this.getRefs.canvasOutput)
          src = output.clone()
        }
        return src
      },
      changeContrastBrightness() {
        if (this.tmp == null) {
          let src = this.sourceImage()
          this.$cv2.imshow(this.$refs.canvasBrightnessContrast, src)
          this.tmp = 1
        }

        // if (src.isContinuous()) {
        //   for (var i = 0; i < src.rows; i++) {
        //     for (var j = 0; j < src.cols; j++) {
        //       let index = i * src.cols * src.channels() + j * src.channels()
        //       for (var c = 0; c < 3; c++) {
        //         src.data[index + c] = this.$utils.clipValue(this.contrastSlider * src.data[index + c] + this.brightnessSlider)
        //       }
        //     }
        //   }
        // }

        // this.noiseMat = src
        // var img = document.getElementById('canvasBrightnessContrast');
        // img.setAttribute('style', 'filter:brightness(' + this.brightnessSlider + '); -webkit-filter:brightness(' + this.brightnessSlider + '); -moz-filter:brightness(' + this.brightnessSlider + ')');
        // console.log("AAAAAAAa")
      },
      init(src) {
        this.$cv2.imshow(this.$refs.canvasBrightnessContrast, src)
      },


    }
  }
</script>

<style scoped>

</style>