<template>
    <v-container>
        <dialog-drag :options='{ buttonClose:false,buttonPin:false,width:500 }'>
            <v-card
            >
                <v-card-title>
                    Kontrast i jasność
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
                                @change="changeBrightnessContrast"
                                :lazy="false"
                                :tooltip="'always'"

                        >
                            <template v-slot:append>
                                <v-subheader class="slider-subheader">{{contrastSlider}}</v-subheader>

                            </template>
                        </v-slider>
                    </v-row>
                    <v-row>
                        <v-subheader class="pl-0">
                            Jasność
                        </v-subheader>

                        <v-slider
                                v-model="brightnessSlider"
                                max="200"
                                min="-200"
                                step="1"
                                :lazy="false"
                                @change="changeBrightnessContrast"
                        >

                            <template v-slot:append>
                                <v-subheader class="slider-subheader">{{brightnessSlider}}</v-subheader>
                            </template>
                        </v-slider>
                    </v-row>
                </v-card-text>
                <v-card-actions>
                    <v-btn
                            text
                            @click="cancelChanges"
                    >
                        Anuluj
                    </v-btn>
                    <v-btn
                            text
                            @click="saveChanges"
                    >
                        Ok
                    </v-btn>
                </v-card-actions>
            </v-card>
        </dialog-drag>
    </v-container>
</template>
<style src='vue-dialog-drag/dist/vue-dialog-drag.css'></style>
<script>
  import {mapActions, mapState} from "vuex";
  import {baseUrl, contrast_and_brightness} from "@/utils/helper";
  import DialogDrag from 'vue-dialog-drag'

  export default {
    name: "brightnessContrast",
    components: {
      DialogDrag
    },
    data: () => {
      return {
        contrastSlider: 1,
        brightnessSlider: 1,
        tmpImage: null
      }
    },
    computed: {
      ...mapState("images", ["backendImageUrl", "dialogs"])
    },
    methods: {
      ...mapActions("images", ["cancelFiltersChangesDialog", "filtersChange"]),
      changeBrightnessContrast() {
        let _this = this
        let params = JSON.stringify(
          {
            "contrast": this.contrastSlider,
            "brightness": this.brightnessSlider
          })
        this.filtersChange({"params": params, "method": contrast_and_brightness,"tmpImage":_this.tmpImage}).then(
          (response) => {
            _this.tmpImage = response.data
          },
          error => {
            console.log(error.response.data)
          }
        );
      },
      saveChanges() {
        let backendUrl = this.backendImageUrl
        this.$store.commit('images/setBackendImageUrl', this.tmpImage)
        this.cancelFiltersChangesDialog({"removeImageUrl": backendUrl, "dialog": "brightnessContrast"})

      },
      cancelChanges() {
        this.$store.commit('images/setCanvasOutput', {
          "url": baseUrl + this.backendImageUrl
        });
        let _this = this
        this.cancelFiltersChangesDialog({"removeImageUrl": _this.tmpImage, "dialog": "brightnessContrast"})
      }
    }
  }
</script>

<style scoped>

</style>