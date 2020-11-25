<template>
    <v-container>
        <v-row>
            <v-menu
                    v-for="(value,key) in menu"
                    :key="key"
                    rounded="0"
                    offset-y
            >
                <template v-slot:activator="{ attrs, on }">
                    <v-btn
                            v-bind="attrs"
                            v-on="on"
                    >
                        {{ key }}
                    </v-btn>
                </template>

                <v-list>
                    <v-list-item
                            v-for="item in value"
                            :key="item['name']"
                            @click="callMethod(item['method'])"
                            link
                    >
                        <v-list-item-title v-text="item['name']"></v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-row>
        <v-row>
            <v-col>
                <img ref="imageSrc" alt="No Image"/>


            </v-col>
            <v-col>
                <canvas ref="canvasOutput"></canvas>
                <div class="caption">canvasOutput</div>
                <v-btn @click="click">AAAAAAAAAAAAAAAA</v-btn>
            </v-col>

        </v-row>
        <upload-image></upload-image>
        <add-noise></add-noise>

    </v-container>

</template>

<script>
  // import NormalDistribution from 'normal-distribution'

  import UploadImage from "./uploadImage";
  import {mapState} from "vuex";
  import AddNoise from "./addNoise";

  export default {

    name: "Images",
    components: {AddNoise, UploadImage},
    data: () => {
      return {
        menu: {
          "Plik": [
            {"name": "Otwórz obraz", "method": "uploadFile"},
            {"name": "Pobierz obraz wynikowy", "method": "downloadFile"}
          ],
          "Zakłócenie": [
            {"name": "Usuń szum", "method": "removeNoise"},
            {"name": "Usuń deszcz", "method": "removeRain"},
            {"name": "Dodaj szum", "method": "addNoise"},
            {"name": "Dodaj efekt deszczu", "method": "addRain"}
          ],
          "Obraz wynikowy": [
            {"name": "Zmień kontrast", "method": "changeContrast"},
            {"name": "Barwa i nasycenie", "method": "hueSaturation"}

          ]
        },
        addNoiseDialog: false,
        noiseStepper: 1,
        addNoiseRadioGroup: null,
        addGaussian: "addGaussian",
        addSP: "addSP",
        addGaussianSigma: 0,
        addSPProbability: 0,
        addNoiseIntensitySlider: 0.02,
        addNoiseIntensityMin: 0,
        addNoiseIntensityMax: 0.2,
        addNoiseIntensityStep: 0.01,
        canvasAddNoiseKey: 1,
        resultMat: null,
        noiseMat: null,
        ref: null
      }
    },
    computed: {
      ...mapState("images", ["fileUploadDialog"])
    },
    created: function () {
      this.$store.commit("images/setImagesRef", this.$refs);
    },
    methods: {
      nextStep() {
        this.noiseStepper = (this.noiseStepper % 2) + 1;
      },
      continueAddNoise() {
        this.nextStep()
        this.addNoiseByType()
      },
      addNoiseByType() {
        this.ref = this.$refs.canvasAddNoise
        if (this.addNoiseRadioGroup === this.addGaussian) {
          this.addGaussianNoise()
        } else {
          this.addSaltPepperNoise()
        }
      },
      cancelAddNoiseDialog() {
        this.addNoiseDialog = false
        this.noiseStepper = 1
        this.addNoiseRadioGroup = null
        this.addGaussianSigma = 0
        this.addSPProbability = 0

      },
      addNoiseSrc() {
        let src
        console.log(this.resultMat)
        if (this.resultMat == null) {
          src = this.$cv2.imread(this.$refs.imageSrc)
        } else {
          let output = this.$cv2.imread(this.$refs.canvasOutput)
          src = output.clone()
        }
        return src
      },
      addGaussianNoisePerChannel(randomNormal, color) {
        let random_normal = randomNormal({mean: 0, dev: this.addNoiseIntensitySlider}) * 255
        let with_noise = random_normal + color
        if (with_noise > 255) {
          with_noise = 255
        }
        if (with_noise < 0) {
          with_noise = 0
        }
        return with_noise
      },
      addGaussianNoise() {
        let src = this.addNoiseSrc()
        var randomNormal = require('random-normal');
        if (src.isContinuous()) {
          for (var i = 0; i < src.rows; i++) {
            for (var j = 0; j < src.cols; j++) {
              let index = i * src.cols * src.channels() + j * src.channels()
              src.data[index] = this.addGaussianNoisePerChannel(randomNormal, src.data[index])
              src.data[index + 1] = this.addGaussianNoisePerChannel(randomNormal, src.data[index + 1])
              src.data[index + 2] = this.addGaussianNoisePerChannel(randomNormal, src.data[index + 2])
            }
          }
        }
        this.$cv2.imshow(this.$refs.canvasAddNoise, src)
        this.noiseMat = src
      }
      ,
      addSaltPepperNoise() {
        let src = this.addNoiseSrc()
        if (src.isContinuous()) {
          for (var i = 0; i < src.rows; i++) {
            for (var j = 0; j < src.cols; j++) {
              let randomNumber = Math.random()
              let index = i * src.cols * src.channels() + j * src.channels()
              let noiseValue = null
              if (randomNumber < (this.addNoiseIntensitySlider / 2)) {
                noiseValue = 0
              } else if (randomNumber < this.addNoiseIntensitySlider) {
                noiseValue = 255
              }
              if (noiseValue != null) {
                src.data[index] = noiseValue
                src.data[index + 1] = noiseValue
                src.data[index + 2] = noiseValue
              }
            }
          }
        }
        this.$cv2.imshow(this.ref, src)
        this.noiseMat = src
      },

      callMethod(method) {
        this.$store.commit("images/" + method);
      }
      // ,
      // addNoise() {
      //   this.addNoiseDialog = true
      // }
      ,
      acceptAddNoise() {
        this.$cv2.imshow(this.$refs.canvasOutput, this.noiseMat)
        this.resultMat = this.noiseMat.clone()
        this.cancelAddNoiseDialog()
      }
      ,
      click() {
        console.log('click')
        let src = this.$cv2.imread(this.$refs.imageSrc)
        console.log(src)
        let gray = new this.$cv2.Mat()
        console.log("gray")
        console.log(gray)
        this.$cv2.cvtColor(src, gray, this.$cv2.COLOR_RGBA2GRAY)
        this.$cv2.imshow(this.$refs.canvasOutput, gray)
      }


    }
  }


</script>

<style scoped>

</style>