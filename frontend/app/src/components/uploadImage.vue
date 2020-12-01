<template>
    <v-container>
        <v-row justify="center">
            <v-dialog
                    v-model="fileUploadDialog"
                    persistent
                    max-width="290"
            >
                <v-card>
                    <v-card-title>
                        Wybierz zdjęcie
                    </v-card-title>
                    <v-card-text>
                        <v-file-input
                                show-size
                                counter
                                v-model="sourceImage"
                                label="Przeglądaj"
                        ></v-file-input>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                                color="green darken-1"
                                text
                                @click="uploadImage"
                        >
                            Otwórz
                        </v-btn>
                        <v-btn
                                text
                                @click="$store.commit('images/cancelUploadFile')"
                        >
                            Anuluj
                        </v-btn>

                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </v-container>
</template>

<script>
  import {mapState, mapActions} from "vuex";

  export default {
    name: "uploadImage",
    data: () => {
      return {
        sourceImage: null
      }
    },
    computed: {
      ...mapState("images", ["fileUploadDialog"]),
    },
    methods: {
      ...mapActions("images", ["newImage"]),
      uploadImage() {
        let _this=this
        this.newImage(_this.sourceImage).then(
          () => {
            console.log("aaaaaaa")
          },
          error => {
            console.log(error.data)
          }
        );
      }
    }
  }
</script>

<style scoped>

</style>