<template>
    <v-container>
        <v-row justify="center">

            <v-dialog
                    v-model="removeNoiseDialog"
                    persistent
                    max-width="590"
            >
                <v-card
                >
                    <v-card-title>
                        Usuń szum
                    </v-card-title>

                    <v-card-subtitle>
                        Wybierz rodzaj szumu
                    </v-card-subtitle>
                    <v-card-text>
                        <noise-type-v-card :remove="true"></noise-type-v-card>
                    </v-card-text>
                    <v-card-actions>

                        <v-btn text @click="$store.commit('images/cancelRemoveNoiseDialog')">
                            Anuluj
                        </v-btn>
                        <v-btn text @click="removeNoise">
                            Ok
                        </v-btn>
                    </v-card-actions>
                </v-card>


            </v-dialog>
        </v-row>
    </v-container>
</template>

<script>
  import {mapState, mapGetters} from "vuex";
  import NoiseTypeVCard from "./base/noiseTypeVCard";
  import axios from "axios";
  import {baseUrl, removeRain, rain} from "@/utils/helper";

  export default {
    name: "removeNoise",
    components: {NoiseTypeVCard},
    data: () => {
      return {
        noiseStepper: 1,
        addNoiseIntensitySlider: 0.02,
        addNoiseIntensityMin: 0,
        addNoiseIntensityMax: 0.2,
        addNoiseIntensityStep: 0.01,
        noiseMat: null,
        noiseImage: null,
        noiseBackendUrl: null

      }
    },
    computed: {
      ...mapState("images", ["removeNoiseDialog", "refs", "resultMat", "noiseRadioGroup", "backendImageUrl", "setBackendImageUrl", "setCanvasOutput",
        "removeRainRadius", "removeRainEpsilon"]),
      ...mapGetters("images", ["getRefs"])
    },
    methods: {

      removeNoise() {
        console.log(removeRain)
        console.log(rain)
        const formData = new FormData();
        formData.append('image_url', this.backendImageUrl)
        if (this.noiseRadioGroup != rain) {
          formData.append("noise", this.noiseRadioGroup)
          axios.post(baseUrl + '/images/remove-noise/', formData).then(response => {
            this.saveChanges(response.data)
          })
            .catch(error => {
              console.log(error)
            })
        } else {
          formData.append("method", removeRain)
          let params = {
            "radius": this.removeRainRadius,
            "epsilon": this.removeRainEpsilon
          }

          formData.append('params', JSON.stringify(params))
          formData.append('old_image', this.backendImageUrl)
          axios.post(baseUrl + '/images/image-processing/', formData).then(response => {
            this.saveChanges(response.data)
          })
            .catch(error => {
              console.log(error)
            })
        }
      },
      saveChanges(data) {
        this.$store.commit('images/setBackendImageUrl', data);
        this.$store.commit('images/setCanvasOutput', {"url":baseUrl + data});
        this.$store.commit('images/cancelRemoveNoiseDialog');
      }

    }
  }
</script>

<style scoped>

</style>