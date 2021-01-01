<template>
    <div>
        <v-radio-group v-model="noiseRadioGroup">
            <v-radio-group
                    v-model="noiseRadioGroup"
                    column
            >
                <v-radio
                        label="Szum gaussowski"
                        :value="gaussian"
                ></v-radio>
                <v-radio
                        label="Szum typu pieprz i sól"
                        :value="sp"
                ></v-radio>
                <v-radio
                        label="Smugi deszczu"
                        :value="rain"
                ></v-radio>
                <v-row v-if="remove && noiseType==='rain'">
                    <v-col>
                        <v-subheader>
                            Podaj wartości parametrów:
                        </v-subheader>
                        <v-text-field v-model="removeRainRadius" label="promień r"  type="number" min="1">
                        </v-text-field>
                        <v-text-field v-model="removeRainEpsilon" label="epsilon"  type="number" step="0.01" min="0.01">
                        </v-text-field>
                    </v-col>
                </v-row>
            </v-radio-group>
        </v-radio-group>
    </div>

</template>

<script>
  import {gaussian, sp, rain} from "@/utils/helper";

  export default {
    name: "noiseTypeVCard",
    props: ["remove"],
    data: () => {
      return {
        gaussian: gaussian,
        sp: sp,
        rain: rain,
        noiseType: null
      }
    },
    computed: {
      noiseRadioGroup: {
        get() {
          return this.$store.state.noiseRadioGroup
        },
        set(value) {
          this.noiseType = value
          this.$store.commit('images/setNoiseRadioGroup', value)
        }
      },
      removeRainRadius: {
        get() {
          return this.$store.state.removeRainRadius || 8
        },
        set(value) {
          this.$store.commit('images/setRemoveRainRadius', value)
        }
      },
      removeRainEpsilon: {
        get() {
          return this.$store.state.removeRainEpsilon || 0.1
        },
        set(value) {
          this.$store.commit('images/setRemoveRainEpsilon', value)
        }
      }
    }
  }
</script>

<style scoped>

</style>