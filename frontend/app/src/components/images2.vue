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
        <v-container>
            <v-row justify="center">
                <v-dialog
                        v-model="fileUploadDialog"
                        persistent
                        max-width="290"
                >
                    <v-card>
                        <v-card-title>
                            Wybierz zdjęcie
                        </v-card-title>
                        <v-card-text>
                            <v-file-input
                                    show-size
                                    counter
                                    v-model="sourceImage"
                                    label="Przeglądaj"
                            ></v-file-input>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                    color="green darken-1"
                                    text
                                    @click="newImage"
                            >
                                Otwórz
                            </v-btn>

                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-row>
        </v-container>
        <v-container>
            <v-row justify="center">
                <v-dialog
                        v-model="addNoiseDialog"
                        persistent
                        max-width="590"
                >
                    <div>
                        <v-stepper v-model="noiseStepper">
                            <v-stepper-header>
                                <template v-for="n in 2">
                                    <v-stepper-step
                                            :key="`${n}-step`"
                                            :complete="n>2"
                                            :step="n"
                                            editable
                                    >
                                        Krok {{ n }}
                                    </v-stepper-step>

                                    <v-divider
                                            v-if="n !== 2"
                                            :key="n"
                                    ></v-divider>
                                </template>
                            </v-stepper-header>

                            <v-stepper-items>
                                <v-stepper-content
                                        step="1"
                                >
                                    <v-card
                                            class="mb-12"
                                    >
                                        <v-card-title>
                                            Wybierz rodzaj szumu
                                        </v-card-title>
                                        <v-card-text>
                                            <v-radio-group v-model="addNoiseRadioGroup">
                                                <v-radio-group
                                                        v-model="addNoiseRadioGroup"
                                                        column
                                                >
                                                    <v-radio
                                                            label="Szum gaussowski"
                                                            :value="addGaussian"
                                                    ></v-radio>
                                                    <v-radio
                                                            label="Szum typu pieprz i sól"
                                                            :value="addSP"
                                                    ></v-radio>
                                                </v-radio-group>
                                            </v-radio-group>
                                        </v-card-text>
                                    </v-card>
                                    <v-btn
                                            color="primary"
                                            @click="nextStep"
                                            disabled
                                            v-if="!addNoiseRadioGroup"
                                    >
                                        Kontunuuj

                                    </v-btn>
                                    <v-btn
                                            color="primary"
                                            @click="continueAddNoise"
                                            v-else
                                    >
                                        Kontunuuj

                                    </v-btn>
                                    <v-btn text @click="cancelAddNoiseDialog">
                                        Anuluj

                                    </v-btn>
                                </v-stepper-content>
                                <v-stepper-content
                                        step="2"
                                >
                                    <v-card
                                            class="mb-12"
                                    >
                                        <v-subheader class="pl-0">
                                            Intensywność szumu
                                        </v-subheader>
                                        <v-slider
                                                v-model="addNoiseIntensitySlider"
                                                :max="addNoiseIntensityMax"
                                                :min="addNoiseIntensityMin"
                                                :step="addNoiseIntensityStep"
                                                @change="addNoiseByType"
                                        >
                                            <template v-slot:append>
                                                <v-text-field
                                                        v-model="addNoiseIntensitySlider"
                                                        class="mt-0 pt-0"
                                                        hide-details
                                                        single-line
                                                        style="width: 60px"
                                                ></v-text-field>
                                            </template>
                                        </v-slider>
                                        <div :key="canvasAddNoiseKey">
                                            <canvas ref="canvasAddNoise"></canvas>
                                        </div>
                                    </v-card>

                                    <v-btn
                                            color="primary"
                                            @click="nextStep"
                                    >
                                        Cofnij
                                    </v-btn>

                                    <v-btn text @click="cancelAddNoiseDialog">
                                        Anuluj
                                    </v-btn>
                                    <v-btn text @click="acceptAddNoise">
                                        Ok
                                    </v-btn>
                                </v-stepper-content>
                            </v-stepper-items>
                        </v-stepper>
                    </div>
                </v-dialog>
            </v-row>
        </v-container>
    </v-container>

</template>

<script>
  // import NormalDistribution from 'normal-distribution'

  export default {

    name: "Images",
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
        fileUploadDialog: false,
        addNoiseDialog: false,
        sourceSrc: "",
        sourceImage: null,
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
    methods: {
      newImage() {
        let imgurl = URL.createObjectURL(this.sourceImage)
        let img = this.$refs.imageSrc
        img.src = imgurl
        console.log('file', this.sourceImage)
        this.fileUploadDialog = false
      },
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
      }
      ,
      uploadFile() {
        this.fileUploadDialog = true
      }
      ,
      callMethod(method, args = []) {
        this[method](...args)
      }
      ,
      addNoise() {
        this.addNoiseDialog = true
      }
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