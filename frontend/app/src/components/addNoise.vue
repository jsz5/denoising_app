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
                                <noise-type-v-card :gaussian="gaussian" :sp="sp"></noise-type-v-card>
                                <v-btn
                                        color="primary"
                                        disabled
                                        v-if="!noiseRadioGroup"
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
                                    <v-img
                                            :src="noiseImage"
                                    >
                                    </v-img>
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
  import NoiseTypeVCard from "./base/noiseTypeVCard";
  import axios from "axios";
  import {baseUrl} from "../utils/helper";

  export default {
    name: "addNoise",
    components: {NoiseTypeVCard},
    data: () => {
      return {
        noiseStepper: 1,
        gaussian: "gaussian",
        sp: "sp",
        addNoiseIntensitySlider: 0.02,
        addNoiseIntensityMin: 0,
        addNoiseIntensityMax: 0.2,
        addNoiseIntensityStep: 0.01,
        noiseMat: null,
        noiseImage: null

      }
    },
    computed: {
      ...mapState("images", ["addNoiseDialog", "refs", "resultMat", "noiseRadioGroup", "backendImageUrl"]),
      ...mapGetters("images", ["getRefs"])
    },
    methods: {

      nextStep() {
        this.noiseStepper = (this.noiseStepper % 2) + 1;
      },
      continueAddNoise() {
        this.nextStep()
        this.setInitialParams()
      },
      setInitialParams() {
        if (this.noiseRadioGroup === this.gaussian) {
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
        console.log("EEEEEEEEEEEEEEEEEEEEds")
        let _this = this
        this.getRefs.canvasOutput.toBlob(function (blob) {
          const formData = new FormData();
          formData.append('file', blob)
          formData.append("noise", _this.noiseRadioGroup)
          formData.append('noise_params', JSON.stringify({"intensity": _this.addNoiseIntensitySlider}))
          formData.append('url', _this.backendImageUrl)
          let __this = _this
          axios.post(baseUrl + '/images/add-noise', formData, {headers: {'Content-Type': 'multipart/form-data'}}).then(response => {
            console.log(response.data)
            __this.noiseImage = baseUrl + response.data
            __this.$store.commit('images/setBackendImageUrl', response.data);
          })
            .catch(error => {
              console.log(error)
            })
        });

      },
      cancelAddNoiseDialog() {
        this.$store.commit('images/cancelAddNoiseDialog')
        this.noiseStepper = 1
        this.$store.commit('images/setNoiseRadioGroup', null)
      },
      acceptAddNoise() {
        // this.$cv2.imshow(this.getRefs.canvasOutput, this.noiseMat)
        // this.newImage(this.noiseImage)
        // this.$store.commit('images/setResultMat', this.noiseMat.clone())
        this.$store.commit('images/setCanvasOutput', this.noiseImage)
        this.cancelAddNoiseDialog()
      }

    }
  }
</script>

<style scoped>

</style>