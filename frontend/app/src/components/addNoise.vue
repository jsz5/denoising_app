<template>
    <v-container>
        <v-row justify="center">
            <v-dialog
                    v-model="dialogs['addNoise']"
                    persistent

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
                                        Dodaj zakłócenie
                                    </v-card-title>

                                    <v-card-subtitle>
                                        Wybierz rodzaj zakłócenia
                                    </v-card-subtitle>
                                    <v-card-text>
                                        <noise-type-v-card :key=noiseRadioGroupKey :remove="false"></noise-type-v-card>
                                    </v-card-text>

                                </v-card>
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
                                <v-btn text @click="cancelDialog">
                                    Anuluj

                                </v-btn>


                            </v-stepper-content>
                            <v-stepper-content
                                    step="2"
                            >
                                <v-card
                                        class="mb-12"
                                >

                                    <v-card-title v-if="noiseRadioGroup=='sp'">
                                        Dodaj szum pieprz i sól
                                        <v-progress-circular v-if="loading"
                                                             :indeterminate="loading"
                                                             color="primary"
                                        ></v-progress-circular>
                                    </v-card-title>
                                    <v-card-title v-if="noiseRadioGroup=='gaussian'">
                                        Dodaj szum gaussowski
                                        <v-progress-circular v-if="loading"
                                                             :indeterminate="loading"
                                                             color="primary"
                                        ></v-progress-circular>
                                    </v-card-title>
                                    <v-card-title v-if="noiseRadioGroup=='rain'">
                                        Dodaj smugi deszczu
                                        <v-progress-circular v-if="loading"
                                                             :indeterminate="loading"
                                                             color="primary"
                                        ></v-progress-circular>
                                    </v-card-title>

                                    <v-card-text v-if="noiseRadioGroup!='rain'">
                                        <v-row>
                                            <v-col>
                                                <v-img
                                                        :src="noiseImage"
                                                >
                                                </v-img>
                                            </v-col>
                                            <v-col>
                                                <v-subheader class="pl-0">
                                                    Intensywność szumu
                                                </v-subheader>
                                                <v-slider
                                                        v-model="addNoiseIntensitySlider"
                                                        max=0.3
                                                        min=0.01
                                                        step=0.01
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
                                            </v-col>

                                        </v-row>
                                    </v-card-text>
                                    <v-card-text v-else>
                                        <v-row>
                                            <v-col>
                                                <v-img
                                                        :src="noiseImage"
                                                >
                                                </v-img>
                                            </v-col>
                                            <v-col>
                                                <v-subheader class="pl-0">
                                                    Kąt padania deszczu
                                                </v-subheader>
                                                <v-slider
                                                        v-model="rainAngleSlider"
                                                        max=3
                                                        min=-3
                                                        step=1
                                                        @change="addNoiseByType"
                                                >
                                                    <template v-slot:append>
                                                        <v-text-field
                                                                v-model="rainAngleSlider"
                                                                class="mt-0 pt-0"
                                                                hide-details
                                                                single-line
                                                                style="width: 60px"
                                                        ></v-text-field>
                                                    </template>
                                                </v-slider>
                                                <v-subheader class="pl-0">
                                                    Długość smug deszczu
                                                </v-subheader>
                                                <v-slider
                                                        v-model="rainKernelSlider"
                                                        max=40
                                                        min=5
                                                        step=1
                                                        @change="addNoiseByType"
                                                >
                                                    <template v-slot:append>
                                                        <v-text-field
                                                                v-model="rainKernelSlider"
                                                                class="mt-0 pt-0"
                                                                hide-details
                                                                single-line
                                                                style="width: 60px"
                                                        ></v-text-field>
                                                    </template>
                                                </v-slider>
                                                <v-subheader class="pl-0">
                                                    Intensywność deszczu
                                                </v-subheader>
                                                <v-slider
                                                        v-model="addNoiseIntensitySlider"
                                                        :max="maxRainIntensity"
                                                        min=0.005
                                                        step=0.005
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
                                            </v-col>
                                        </v-row>
                                    </v-card-text>

                                </v-card>

                                <v-btn
                                        color="primary"
                                        @click="nextStep"
                                >
                                    Cofnij
                                </v-btn>

                                <v-btn text @click="cancelAddNoiseDialog(noiseBackendUrl)">
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
  import {mapState} from "vuex";
  import NoiseTypeVCard from "./base/noiseTypeVCard";
  import axios from "axios";
  import {baseUrl, gaussian, sp, rain} from "../utils/helper";

  export default {
    name: "addNoise",
    components: {NoiseTypeVCard},
    data: () => {
      return {
        noiseStepper: 1,
        addNoiseIntensitySlider: 0.3,
        rainAngleSlider: 1,
        rainKernelSlider: 5,
        maxRainIntensity: 0.1,
        noiseImage: null,
        noiseBackendUrl: null,
        loading: false,
        rainRadius: 8,
        rainEpsilon: 0.1,
        noiseRadioGroupKey:1
      }
    },
    computed: {
      ...mapState("images", ["dialogs", "noiseRadioGroup", "backendImageUrl"])
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
        if (this.noiseRadioGroup === gaussian) {
          this.addNoiseIntensitySlider = 0.05
        } else if (this.noiseRadioGroup === sp) {
          this.addNoiseIntensitySlider = 0.02
        }
        this.addNoiseByType()
      },
      addNoiseByType() {
        if (Math.abs(this.rainAngleSlider) === 2) {
          this.maxRainIntensity = 0.2
        } else if (Math.abs(this.rainAngleSlider) === 3) {
          this.maxRainIntensity = 0.3
        }
        this.loading = true
        let _this = this
        const formData = new FormData();
        formData.append('image_url', this.backendImageUrl)
        formData.append("method", this.noiseRadioGroup)
        let params = {"intensity": this.addNoiseIntensitySlider}
        if (this.noiseRadioGroup === rain) {
          params["kernel_size"] = this.rainKernelSlider
          params["angle"] = this.rainAngleSlider
        }
        formData.append('params', JSON.stringify(params))
        formData.append('old_image', this.noiseBackendUrl)
        axios.post(baseUrl + '/images/image-processing/', formData).then(response => {
          console.log(response.data)
          _this.noiseImage = baseUrl + response.data
          _this.noiseBackendUrl = response.data
          _this.loading = false
        })
          .catch(error => {
            console.log(error.response.data)
          })
      },

      cancelAddNoiseDialog(oldImageUrl) {
        this.cancelDialog()
        axios.post(baseUrl + '/images/remove-image/', {"image_url": oldImageUrl}).catch(error => {
          console.log(error.response.data)
        })
        this.noiseStepper = 1
        this.noiseImage = null
        this.noiseBackendUrl = null
      },
      cancelDialog(){
         this.$store.commit('images/closeDialog', 'addNoise')
         this.noiseRadioGroupKey+=1
      },
      acceptAddNoise() {
        let backendUrl = this.backendImageUrl
        this.$store.commit('images/setBackendImageUrl', this.noiseBackendUrl)
        this.$store.commit('images/setCanvasOutput', {"url": baseUrl + this.noiseBackendUrl})
        this.cancelAddNoiseDialog(backendUrl)
      }

    }
  }
</script>

<style scoped>

</style>