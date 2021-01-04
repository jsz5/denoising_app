<template>
    <v-container>
        <dialog-drag :options='{ buttonClose:false,buttonPin:false,width:400 }'>
            <v-card
            >
                <v-card-title>
                    Barwa i nasycenie
                </v-card-title>
                <v-card-text>

                    <v-row>
                        <v-subheader class="pl-0">
                            Kolor czerwony
                        </v-subheader>
                        <v-slider
                                v-model="redSlider"
                                max="3"
                                min="0"
                                step="0.01"
                                :lazy="false"
                                :tooltip="'always'"
                                @change="changeHueSaturation"

                        >
                            <template v-slot:append>
                                <v-subheader class="slider-subheader">
                                    {{redSlider}}
                                </v-subheader>

                            </template>
                        </v-slider>
                    </v-row>
                    <v-row>
                        <v-subheader class="pl-0">
                            Kolor zielony
                        </v-subheader>
                        <v-slider
                                v-model="greenSlider"
                                max="3"
                                min="0"
                                step="0.01"
                                :lazy="false"
                                :tooltip="'always'"
                                @change="changeHueSaturation"

                        >
                            <template v-slot:append>
                                <v-subheader class="slider-subheader">
                                    {{greenSlider}}
                                </v-subheader>

                            </template>
                        </v-slider>
                    </v-row>
                    <v-row>
                        <v-subheader class="pl-0">
                            Kolor niebieski
                        </v-subheader>
                        <v-slider
                                v-model="blueSlider"
                                max="3"
                                min="0"
                                step="0.01"
                                :lazy="false"
                                :tooltip="'always'"
                                @change="changeHueSaturation"

                        >
                            <template v-slot:append>
                                <v-subheader class="slider-subheader">
                                    {{blueSlider}}
                                </v-subheader>

                            </template>
                        </v-slider>
                    </v-row>
                    <v-row>
                        <v-subheader class="pl-0">
                            Nasycenie
                        </v-subheader>
                        <v-slider
                                v-model="saturationSlider"
                                max="3"
                                min="0"
                                step="0.01"
                                :lazy="false"
                                @change="changeHueSaturation"
                        >

                            <template v-slot:append>
                                <v-subheader class="slider-subheader">
                                    {{saturationSlider}}
                                </v-subheader>

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
  import {baseUrl, color_balance} from "@/utils/helper";
  import DialogDrag from "vue-dialog-drag";


  export default {
    name: "hueSaturation",
    components: {
      DialogDrag
    },

    data: () => {
      return {
        redSlider: 1,
        greenSlider: 1,
        blueSlider: 1,
        saturationSlider: 1,
        tmpImage: null
      }
    },
    computed: {
      ...mapState("images", ["backendImageUrl", "dialogs"])
    },
    methods: {
      ...mapActions("images", ["cancelFiltersChangesDialog", "filtersChange"]),
      changeHueSaturation() {
        let _this = this
        let params = JSON.stringify(
          {
            "red": this.redSlider,
            "green": this.greenSlider,
            "blue": this.blueSlider,
            "saturation": this.saturationSlider,
          })
        this.filtersChange({"params": params, "method": color_balance,"tmpImage":_this.tmpImage}).then(
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
        this.cancelFiltersChangesDialog({"removeImageUrl": backendUrl, "dialog": "hueSaturation"})

      },
      cancelChanges() {
        this.$store.commit('images/setCanvasOutput', {
          "url": baseUrl + this.backendImageUrl
        });
        let _this = this
        this.cancelFiltersChangesDialog({"removeImageUrl": _this.tmpImage, "dialog": "hueSaturation"})
      }
    }
  }
</script>

<style scoped>

</style>