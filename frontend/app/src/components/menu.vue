<template>
    <v-row class="menuRow">
        <v-menu
                v-for="(value,key) in menu"
                :key="key"
                rounded="0"
                offset-y
        >
            <template v-slot:activator="{ attrs, on }">
                <v-btn  class="menuButton"
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
</template>

<script>
  import axios from "axios";
  import {mapState} from "vuex";
  import {baseUrl} from "@/utils/helper";

  export default {
    name: "ImageMenu",
    data: () => ({
      menu: {
        "Plik": [
          {"name": "Otwórz obraz", "method": "uploadFile"},
          {"name": "Pobierz obraz wynikowy", "method": "downloadFile"}
        ],
        "Zakłócenie": [
          {"name": "Usuń szum", "method": "removeNoise"},
          {"name": "Dodaj szum", "method": "addNoise"}
        ],
        "Obraz wynikowy": [
          {"name": "Kontrast i jasność", "method": "brightnessContrast"},
          {"name": "Barwa i nasycenie", "method": "hueSaturation"}
        ]
      }
    }),
    computed: {
      ...mapState("images", ["backendImageUrl"]),
    },
    methods: {
      callMethod(method) {
        if (method !== "downloadFile") {
          this.$store.commit("images/openDialog", method);
        } else {
          const formData = new FormData();
          formData.append("image_url", this.backendImageUrl)
          axios.get(baseUrl+this.backendImageUrl, {responseType: 'blob'})
            .then(response => {
              const blob = new Blob([response.data], {type:"image/png"})
              const link = document.createElement('a')
              link.href = URL.createObjectURL(blob)
              link.download = "download"
              link.click()
              URL.revokeObjectURL(link.href)
            }).catch(console.error)
        }

      }

    }
  }
</script>


<style scoped>


</style>