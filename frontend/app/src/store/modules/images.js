import axios from "axios";
import {baseUrl} from "../../utils/helper";

const state = {
  refs: null,
  fileUploadDialog: false,
  addNoiseDialog: false,
  removeNoiseDialog: false,
  resultMat: null,
  noiseRadioGroup: null,
  showFilter: null,
  resultImageBlob: null,
  backendImageUrl: null,
  removeRainEpsilon: 0.1,
  removeRainRadius: 8
};

const actions = {
  newImage(store, sourceImage) {

    const formData = new FormData();
    formData.append('new_image', sourceImage)
    return new Promise((resolve, reject) => {
      axios.post(baseUrl + '/images/upload/', formData, {headers: {'Content-Type': 'multipart/form-data'}})
        .then(function (response) {
          resolve(response);
          console.log(baseUrl + response.data)
          store.commit('setBackendImageUrl', response.data);
          let url = URL.createObjectURL(sourceImage)
          store.commit('setImageRefSrc', url);
          let urlWithBase=baseUrl+response.data
          store.commit('setCanvasOutput', {"url":urlWithBase});
          store.commit('cancelUploadFile');
          console.log(response.data)
        })
        .catch(function (error) {
          reject(error);
        });state.refs.canvasOutput
    })
  },
  saveFiltersChange(store) {
    let dataURL=state.refs.canvasOutput.toDataURL('image/png')
    const formData = new FormData();
    formData.append('file', dataURL)
    formData.append('old_url', state.backendImageUrl)
    return new Promise((resolve, reject) => {
      axios.post(baseUrl + '/images/save-image/', formData, {
        headers: {
          'Content-Type': "multipart/form-data"
        }
      }).then(response => {
        store.commit('setBackendImageUrl', response.data)
        store.commit('cancelFilter');
        store.commit('setCanvasOutput', {"url":baseUrl + response.data})

        resolve(response);
      }).catch(function (error) {
        reject(error);
      });
    })

  }

};


const getters = {
  getRefs(state) {
    return state.refs
  }
};


const mutations = {
  setImagesRef(state, refs) {
    state.refs = refs
  },
  setCanvasOutput(state, {url, filters=null}) {
    console.log(url)
    var img = new Image();
    img.onload = function () {
      var ctx = state.refs.canvasOutput.getContext('2d');
      ctx.canvas.width = img.width
      ctx.canvas.height = img.height
      if (filters) {
        ctx.filter = filters
      }
      ctx.drawImage(img, 0, 0);
    }
    img.crossOrigin = "anonymous"
    img.src = url
    console.log(img.src)

  },
  setOutputCanvas(imageUrl) {
    var img = new Image();
    img.onload = function () {
      var ctx = state.refs.canvasOutput.getContext('2d');
      ctx.drawImage(img, 0, 0);
    }
    img.crossOrigin = "anonymous"
    img.src = imageUrl
  },
  setOutputAsResult(state) {
    state.resultImageBlob = state.refs.canvasOutput.toDataURL()
    state.showBrightnessContrast = false
  },
  uploadFile(state) {
    state.fileUploadDialog = true
  },
  removeNoise(state) {
    state.removeNoiseDialog = true
  },
  cancelUploadFile(state) {
    state.fileUploadDialog = false
  },
  addNoise(state) {
    state.addNoiseDialog = true
  },
  cancelAddNoiseDialog(state) {
    state.addNoiseDialog = false
  },
  cancelRemoveNoiseDialog(state) {
    state.removeNoiseDialog = false
  },
  brightnessContrast(state) {
    state.showFilter = "brightnessContrast"
    state.refs.canvasOutput.setAttribute('style', 'filter:brightness(1) contrast(1) hue-rotate(1) saturate(1)');

  },
  hueSaturation(state) {
    state.showFilter = "hueSaturation"
    state.refs.canvasOutput.setAttribute('style', 'filter:brightness(1) contrast(1) hue-rotate(1) saturate(1)');
  },

  cancelFilter(state) {
    state.showFilter = null
    state.refs.canvasOutput.setAttribute('style', 'filter:brightness(1) contrast(1) hue-rotate(1) saturate(1)');

  },
  setResultMat(state, result) {
    state.resultMat = result
  },
  setNoiseRadioGroup(state, value) {
    state.noiseRadioGroup = value
  },
  setInitialContrast(state) {
    state.initialContrast = false
  },
  setRemoveRainRadius(state, value) {
    state.removeRainRadius = value
  },
  removeRainEpsilon(state, value) {
    state.removeRainEpsilon = value
  },
  setBackendImageUrl(state, url) {
    state.backendImageUrl = url
    console.log("backend result")
    console.log(state.backendImageUrl)
  },
  setResultImageBlob(state, url) {
    state.resultImageBlob = url
  },
  setImageRefSrc(state, url) {
    state.refs.imageSrc.src = url
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
