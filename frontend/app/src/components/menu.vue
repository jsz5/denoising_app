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
                        :key="item"
                        link
                >
                    <v-list-item-title v-text="item"></v-list-item-title>
                </v-list-item>
            </v-list>
        </v-menu>
    </v-row>
</template>

<script>
  export default {
    name: "Menu",
    data: () => ({
      menu: {
        "Plik": ["Otwórz", "Pobierz"],
        "Zakłócenie": ["Usuń szum", "Usuń deszcz"],
        "Obraz": [ "Zmień kontrast", "Barwa i nasycenie","Dodaj szum", "Dodaj efekt deszczu"]
      }
    }),
  }
</script>


<style scoped>


</style>