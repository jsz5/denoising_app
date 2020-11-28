<template>
    <v-container>
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
                    @click="$store.commit('images/cancelFilter')"
            >
                Anuluj
            </v-btn>
        </v-row>
    </v-container>
</template>

<script>
  import {mapGetters} from "vuex";


  export default {
    name: "brightnessContrast",


    data: () => {
      return {
        contrastSlider: 1,
        brightnessSlider: 1,
      }
    },
    computed: {
      ...mapGetters("images", ["getRefs"])
    },
    watch: {
      brightnessSlider() {
        this.changeBrightnessContrast()
      },
      contrastSlider() {
        this.changeBrightnessContrast()
      }
    },
    methods: {
      changeBrightnessContrast() {
        var img = this.getRefs.canvasOutput
        img.setAttribute('style', 'filter:brightness(' + this.brightnessSlider + ') contrast(' + this.contrastSlider + ')')

      },
      saveChanges(){
        let filters="brightness(" + this.brightnessSlider + ")contrast(" + this.contrastSlider + ")"
        this.$store.dispatch('images/saveFiltersChange',filters)
      }
    }
  }
</script>

<style scoped>

</style>