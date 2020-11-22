<template>
    <v-row>
        <div>
            <div class="inputoutput">
                <img ref="imageSrc" alt="No Image"/>
                <div class="caption">imageSrc <input type="file" id="fileInput" name="file"
                                                     @change="newimg($event.target.files[0])"/></div>
            </div>
            <div class="inputoutput">
                <canvas ref="canvasOutput"></canvas>
                <div class="caption">canvasOutput</div>
            </div>
            <v-btn @click="click">AAAAAAAAAAAAAAAA</v-btn>
        </div>
    </v-row>
</template>

<script>
  export default {
    name: "Images",
    data: () => {
      return {
        sourceSrc: ""
      }
    },
    methods: {
      newimg(file) {
        let imgurl = URL.createObjectURL(file)
        let img = this.$refs.imageSrc
        img.src = imgurl
        console.log('file', file);
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