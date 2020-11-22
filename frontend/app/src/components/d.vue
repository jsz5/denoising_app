<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div>
      <input type="file" id="file" :name="files" @change="newimg" accept="image/*"/>
      <button @click="click">Try</button>
    </div>
    <div>
      <canvas id="srcimg" ref="srcimg" class="imgcanvas"></canvas>
      <canvas id="dstimg" ref="dstimg" class="imgcanvas"></canvas>
      <img src="" ref="img" class="img"/>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Main',
  props: {
    msg: String
  },
  data () {
    return {
      faceClass: null,
      eyeClass: null,
      files: []
    }
  },
  precreate () {
  },
  created () {


  },
  mounted () {
    this.loadImg()
    let requestFileSystem = window.requestFileSystem || window.webkitRequestFileSystem;
     requestFileSystem(window.TEMPORARY, 1024*1024, (fs) => {
      console.log(fs)
      let rdr = fs.root.createReader()

      rdr.readEntries((rslt) => {
        console.log(rslt)
        for (let itm of rslt) {
          console.log(itm);
        }
      })
    })
  },
  methods: {
    newimg(evt) {
      let files = evt.target.files
      if (!files.length) return
      let imgurl = URL.createObjectURL(files[0])
      let img = this.$refs.img
      img.src = imgurl
      console.log('file',files[0]);
    },
    click() {
      console.log('click')
      let src = this.$cv2.imread(this.$refs.srcimg)
      let gray = new this.$cv2.Mat()
      this.$cv2.cvtColor(src,gray, this.$cv2.COLOR_RGBA2GRAY)
      let faces = new this.$cv2.RectVector()
      let eyes = new this.$cv2.RectVector()
      let msize = new this.$cv2.Size(0,0)
      this.faceClass.detectMultiScale(gray, faces, 1.1, 3,0, msize, msize)
      for (let i=0;i<faces.size();i++) {
        let roiGray = gray.roi(faces.get(i))
        let roiSrc = src.roi(faces.get(i))
        let point1 = new this.$cv2.Point(faces.get(i).x, faces.get(i).y);
        let point2 = new this.$cv2.Point(faces.get(i).x + faces.get(i).width,
                              faces.get(i).y + faces.get(i).height);
        this.$cv2.rectangle(src, point1, point2, [255, 0, 0, 255]);
        this.eyeClass.detectMultiScale(roiGray, eyes);
        for (let j = 0; j < eyes.size(); ++j) {
          let point1 = new this.$cv2.Point(eyes.get(j).x, eyes.get(j).y);
          let point2 = new this.$cv2.Point(eyes.get(j).x + eyes.get(j).width,
                                  eyes.get(j).y + eyes.get(j).height);
          this.$cv2.rectangle(roiSrc, point1, point2, [0, 0, 255, 255]);
        }
        roiGray.delete(); roiSrc.delete();
      }
      this.$cv2.imshow(this.$refs.dstimg, src)
      src.delete();gray.delete();faces.delete(); eyes.delete();
    },

    loadImg(){
      let src = this.$refs.srcimg
      let ctx = src.getContext('2d')
      let img = this.$refs.img //new Image()
      img.onload = function() {
        src.height = img.height
        src.width = img.width
        ctx.drawImage(img, 0 ,0)
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.imgcanvas {
  width: 256px;
  height: 256px;
  border: 2px solid #000;
  margin: 10px;
}
.img {
  visibility: hidden;
}
#file {
  float: left;
}
</style>