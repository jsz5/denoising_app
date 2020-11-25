<template>
    <v-card
            class="mb-12"
    >
        <v-card-title>
            Wybierz rodzaj szumu
        </v-card-title>
        <v-card-text>
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
                </v-radio-group>
            </v-radio-group>
        </v-card-text>
    </v-card>
</template>

<script>
  export default {
    name: "noiseTypeVCard",
    props: ['gaussian', 'sp'],
    computed: {
      noiseRadioGroup: {
        get() {
          return this.$store.state.noiseRadioGroup
        },
        set(value) {
          this.$store.commit('images/setNoiseRadioGroup', value)
        }
      }
    }
  }
</script>

<style scoped>

</style>