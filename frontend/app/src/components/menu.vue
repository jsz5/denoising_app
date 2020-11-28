<template>
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
</template>

<script>
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
          {"name": "Usuń deszcz", "method": "removeRain"},
          {"name": "Dodaj szum", "method": "addNoise"},
          {"name": "Dodaj efekt deszczu", "method": "addRain"}
        ],
        "Obraz wynikowy": [
          {"name": "Zmień kontrast i jasność", "method": "brightnessContrast"},
          {"name": "Barwa i nasycenie", "method": "hueSaturation"}
        ]
      }
    }),
    methods: {
      callMethod(method) {
        this.$store.commit("images/" + method);
      }
    }
  }
</script>


<style scoped>


</style>