import axios from "axios";
import {baseUrl} from "../../utils/helper";

const state = {
  refs: null,
  fileUploadDialog: false,
  addNoiseDialog: false,
  resultMat: null,
  noiseRadioGroup: null,
  showFilter: null,
  resultImageBlob: null,
  backendImageUrl: null


};

const actions = {
  newImage(store, sourceImage) {
    const formData = new FormData();
    formData.append('file', sourceImage)
    return new Promise((resolve, reject) => {
      axios.post(baseUrl + '/images/upload', formData, {headers: {'Content-Type': 'multipart/form-data'}})
        .then(function (response) {
          resolve(response);
          store.commit('setBackendImageUrl', response.data);
          store.commit('setResultImageBlob', URL.createObjectURL(sourceImage));
          let url = URL.createObjectURL(sourceImage)
          store.commit('setImageRefSrc', url);
          store.commit('setCanvasOutput', url);
          store.commit('cancelUploadFile');
          console.log(response.data)
        })
        .catch(function (error) {
          reject(error);
        });
    })
  },
  saveFiltersChange(store, payload) {
    store.commit('setFiltersChange', payload);
    store.commit('cancelFilter');

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
  setCanvasOutput(state, url) {
    var img = new Image();
    img.onload = function () {
      var ctx = state.refs.canvasOutput.getContext('2d');
      ctx.canvas.width = img.width
      ctx.canvas.height = img.height
      ctx.drawImage(img, 0, 0);
    }
    img.src = url
  },
  setOutputCanvas(imageUrl) {
    var img = new Image();
    img.onload = function () {
      var ctx = state.refs.canvasOutput.getContext('2d');
      ctx.drawImage(img, 0, 0);
    }
    img.src = imageUrl
  },
  setOutputAsResult(state) {
    state.resultImageBlob = state.refs.canvasOutput.toDataURL()
    state.showBrightnessContrast = false
  },
  uploadFile(state) {
    state.fileUploadDialog = true
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
  brightnessContrast(state) {
    state.showFilter = "brightnessContrast"
    state.refs.canvasOutput.setAttribute('style', 'filter:brightness(1) contrast(1) hue-rotate(1) saturate(1)');

  },
  hueSaturation(state) {
    state.showFilter = "hueSaturation"
    state.refs.canvasOutput.setAttribute('style', 'filter:brightness(1) contrast(1) hue-rotate(1) saturate(1)');
  },
  setFiltersChange(state, filters) {
    var img = new Image();
    img.onload = function () {
      var ctx = state.refs.canvasOutput.getContext('2d');
      ctx.filter = filters
      ctx.drawImage(img, 0, 0);
      state.refs.canvasOutput.toBlob(function (blob) {
        state.resultImageBlob = URL.createObjectURL(blob);
      });
    }
    img.src = state.resultImageBlob

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
  setBackendImageUrl(state, url) {
    state.backendImageUrl = url
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
