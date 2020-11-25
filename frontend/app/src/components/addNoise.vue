<template>
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
                                    <div>
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
</template>

<script>
  import {mapState, mapGetters} from "vuex";

  export default {
    name: "addNoise",
    data: () => {
      return {
        noiseStepper: 1,
        addNoiseRadioGroup: null,
        addGaussian: "addGaussian",
        addSP: "addSP",
        addNoiseIntensitySlider: 0.02,
        addNoiseIntensityMin: 0,
        addNoiseIntensityMax: 0.2,
        addNoiseIntensityStep: 0.01,
        noiseMat: null,
      }
    },
    computed: {
      ...mapState("images", ["addNoiseDialog", "refs", "resultMat"]),
      ...mapGetters("images",["getRefs"])
    },
    methods: {
      nextStep() {
        this.noiseStepper = (this.noiseStepper % 2) + 1;
      },
      continueAddNoise() {
        this.nextStep()
        this.setInitialParams()
      },
      setInitialParams(){
        if (this.addNoiseRadioGroup === this.addGaussian) {
          this.addNoiseIntensitySlider = 0.05
          this.addNoiseIntensityMin = 0
          this.addNoiseIntensityMax = 0.3
        } else {
          this.addNoiseIntensitySlider = 0.02
          this.addNoiseIntensityMin = 0
          this.addNoiseIntensityMax = 0.2
        }
        this.addNoiseByType()
      },
      addNoiseByType() {
        if (this.addNoiseRadioGroup === this.addGaussian) {
          this.addGaussianNoise()
        } else {
          this.addSaltPepperNoise()
        }
      },
      cancelAddNoiseDialog() {
        this.$store.commit('images/cancelAddNoiseDialog')
        this.noiseStepper = 1
        this.addNoiseRadioGroup = null
      },
      addNoiseSrc() {
        let src
        if (this.resultMat == null) {
          src = this.$cv2.imread(this.getRefs.imageSrc)
        } else {
          let output = this.$cv2.imread(this.getRefs.canvasOutput)
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
        this.$cv2.imshow(this.$refs.canvasAddNoise, src)
        this.noiseMat = src
      },
      acceptAddNoise() {
        this.$cv2.imshow(this.getRefs.canvasOutput, this.noiseMat)
        this.$store.commit('images/setResultMat',this.noiseMat.clone())
        this.cancelAddNoiseDialog()
      }

    }
  }
</script>

<style scoped>

</style>