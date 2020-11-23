<template>
    <v-container>
        <v-row>
            <v-menu
                    v-for="(value,key) in menu"
                    :key="key"
                    rounded="0"
                    offset-y
            >
                <template v-slot:activator="{ attrs, on }">
                    <v-btn
                            v-bind="attrs"
                            v-on="on"
                    >
                        {{ key }}
                    </v-btn>
                </template>

                <v-list>
                    <v-list-item
                            v-for="item in value"
                            :key="item['name']"
                            @click="callMethod(item['method'])"
                            link
                    >
                        <v-list-item-title v-text="item['name']"></v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
        </v-row>
        <v-row>
            <v-col>
                <img ref="imageSrc" alt="No Image"/>


            </v-col>
            <v-col>
                <canvas ref="canvasOutput"></canvas>
                <div class="caption">canvasOutput</div>
                <v-btn @click="click">AAAAAAAAAAAAAAAA</v-btn>
            </v-col>

        </v-row>
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
                                    @click="newImage"
                            >
                                Otwórz
                            </v-btn>

                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-row>
        </v-container>
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
                                    <v-card
                                            class="mb-12"
                                    >
                                        <v-card-title>
                                            Wybierz rodzaj szumu
                                        </v-card-title>
                                        <v-card-text>
                                            <v-radio-group v-model="addNoiseRadioGroup">
                                                <v-radio-group
                                                        v-model="addNoiseRadioGroup"
                                                        column
                                                >
                                                    <v-radio
                                                            label="Szum gaussowski"
                                                            :value="addGaussian"
                                                    ></v-radio>
                                                    <v-radio
                                                            label="Szum typu pieprz i sól"
                                                            :value="addSP"
                                                    ></v-radio>
                                                </v-radio-group>
                                            </v-radio-group>
                                        </v-card-text>
                                    </v-card>
                                    <v-btn
                                            color="primary"
                                            @click="nextStep"
                                            disabled
                                            v-if="!addNoiseRadioGroup"
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
                                        <canvas ref="canvasAddNoise"></canvas>
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
                                </v-stepper-content>
                            </v-stepper-items>
                        </v-stepper>
                    </div>
                </v-dialog>
            </v-row>
        </v-container>
    </v-container>

</template>

<script>
  export default {
    name: "Images",
    data: () => {
      return {
        menu: {
          "Plik": [
            {"name": "Otwórz obraz", "method": "uploadFile"},
            {"name": "Pobierz obraz wynikowy", "method": "downloadFile"}
          ],
          "Zakłócenie": [
            {"name": "Usuń szum", "method": "removeNoise"},
            {"name": "Usuń deszcz", "method": "removeRain"}
          ],
          "Obraz": [
            {"name": "Zmień kontrast", "method": "changeContrast"},
            {"name": "Barwa i nasycenie", "method": "hueSaturation"},
            {"name": "Dodaj szum", "method": "addNoise"},
            {"name": "Dodaj efekt deszczu", "method": "addRain"}
          ]
        },
        fileUploadDialog: false,
        addNoiseDialog: false,
        sourceSrc: "",
        sourceImage: null,
        noiseStepper: 1,
        addNoiseRadioGroup: null,
        addGaussian: "addGaussian",
        addSP: "addSP",
        addGaussianSigma: 0,
        addSPProbability: 0,
        addNoiseIntensitySlider: 1,
        addNoiseIntensityMin: 0,
        addNoiseIntensityMax: 1,
        addNoiseIntensityStep: 0.01,
      }
    },
    methods: {
      newImage() {
        let imgurl = URL.createObjectURL(this.sourceImage)
        let img = this.$refs.imageSrc
        img.src = imgurl
        console.log('file', this.sourceImage)
        this.fileUploadDialog = false
      },
      nextStep() {
        this.noiseStepper = (this.noiseStepper % 2) + 1;
      },
      continueAddNoise() {
        this.nextStep()
        console.log(this.addNoiseRadioGroup)
        if (this.addNoiseRadioGroup === this.addGaussian) {
          console.log("LLLL")
          this.addGaussianNoise()
        } else {
          console.log("KKK")
          this.addSaltPepperNoise()
        }

      },
      cancelAddNoiseDialog() {
        this.addNoiseDialog = false
        this.noiseStepper = 1
        this.addNoiseRadioGroup = null
        this.addGaussianSigma = 0
        this.addSPProbability = 0

      },
      addGaussianNoise() {
        console.log("rrrr")
        let src = this.$cv2.imread(this.$refs.imageSrc)
        let row = 37, col = 34;

        if (src.isContinuous()) {
          let R = src.data[row * src.cols * src.channels() + col * src.channels()];
          let G = src.data[row * src.cols * src.channels() + col * src.channels() + 1];
          let B = src.data[row * src.cols * src.channels() + col * src.channels() + 2];
          console.log(R, G, B)
          src.data[row * src.cols * src.channels() + col * src.channels()] = 0
          G = 0
          B = 0
          let R2 = src.data[row * src.cols * src.channels() + col * src.channels()];
          let G2 = src.data[row * src.cols * src.channels() + col * src.channels() + 1];
          let B2 = src.data[row * src.cols * src.channels() + col * src.channels() + 2];
          console.log(R2, G2, B2)
        }


        // let A = src.ucharAt(row, col * src.channels() + 3);
        console.log("uuuuu")
        //
        // let R2 = src.ucharAt(row, col * src.channels());
        // let G2 = src.ucharAt(row, col * src.channels() + 1);
        // let B2 = src.ucharAt(row, col * src.channels() + 2);
        // console.log(R2, G2, B2)


        console.log("ppppp")


        // this.$cv2.cvtColor(src, gray, this.$cv2.COLOR_RGBA2GRAY)
        // this.$cv2.imshow(this.$refs.canvasAddNoise, gray)        // this.$cv2.cvtColor(src, gray, this.$cv2.COLOR_RGBA2GRAY)
        this.$cv2.imshow(this.$refs.canvasAddNoise, src)
      },
      addSaltPepperNoise() {

      },
      uploadFile() {
        this.fileUploadDialog = true
        console.log("FFF")
      }
      ,
      callMethod(method, args = []) {
        console.log("KKK")
        this[method](...args)
      },
      addNoise() {
        this.addNoiseDialog = true
      },
      click() {
        console.log('click')
        let src = this.$cv2.imread(this.$refs.imageSrc)
        console.log(src)
        let gray = new this.$cv2.Mat()
        console.log("gray")
        console.log(gray)
        this.$cv2.cvtColor(src, gray, this.$cv2.COLOR_RGBA2GRAY)
        this.$cv2.imshow(this.$refs.canvasOutput, gray)
      }


    }
  }


</script>

<style scoped>

</style>