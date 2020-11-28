<template>
    <v-container>
        <v-row>
            <v-subheader class="pl-0">
                Barwa
            </v-subheader>
            <v-slider
                    v-model="hueSlider"
                    max="1"
                    min="0"
                    step="0.01"
                    :lazy="false"
                    :tooltip="'always'"

            >
                <template v-slot:append>
                    <v-text-field
                            v-model="hueSlider"
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
                Nasycenie
            </v-subheader>
            <v-slider
                    v-model="saturationSlider"
                    max="5"
                    min="0"
                    step="0.01"
                    :lazy="false"
            >

                <template v-slot:append>
                    <v-text-field
                            v-model="saturationSlider"
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
    name: "hueSaturation",


    data: () => {
      return {
        hueSlider: 1,
        saturationSlider: 1,
      }
    },
    computed: {
      ...mapGetters("images", ["getRefs"])
    },
    watch: {
      hueSlider() {
        this.changeHueSaturation()
      },
      saturationSlider() {
        this.changeHueSaturation()
      }
    },
    methods: {
      changeHueSaturation() {
        var img = this.getRefs.canvasOutput
        img.setAttribute('style', 'filter:hue-rotate(' + this.hueSlider + 'turn)'+' saturate(' + this.saturationSlider + ')')


      },
      saveChanges(){
        let filters="hue-rotate(" + this.hueSlider + "turn)saturate(" + this.saturationSlider + ")"
        this.$store.dispatch('images/saveFiltersChange',filters)
      }
    }
  }
</script>

<style scoped>

</style>