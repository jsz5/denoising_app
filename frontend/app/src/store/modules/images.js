import axios from "axios";
import {baseUrl} from "../../utils/helper";

const state = {
  refs: null,
  dialogs: {
    "uploadFile": false,
    "addNoise": false,
    "removeNoise": false,
    "brightnessContrast": false,
    "hueSaturation": false
  },
  noiseRadioGroup: null,
  backendImageUrl: null,
  removeRainEpsilon: 0.1,
  removeRainRadius: 8,
};

const actions = {
  newImage(store, sourceImage) {
    const formData = new FormData();
    formData.append('new_image', sourceImage)
    return new Promise((resolve, reject) => {
      axios.post(baseUrl + '/images/upload/', formData, {headers: {'Content-Type': 'multipart/form-data'}})
        .then(function (response) {
          store.commit('setBackendImageUrl', response.data);
          let url = URL.createObjectURL(sourceImage)
          store.commit('setImageRefSrc', url);
          let urlWithBase = baseUrl + response.data
          store.commit('setCanvasOutput', {"url": urlWithBase});
          store.commit('closeDialog', 'uploadFile');
          resolve(response);
        })
        .catch(function (error) {
          reject(error);
        });
      state.refs.canvasOutput
    })
  },
  filtersChange(store, {params, method}) {
    const formData = new FormData();
    let backendImageUrl = store.getters.getBackendImageUrl
    formData.append('image_url', backendImageUrl)
    formData.append("method", method)
    formData.append('params', params)
    return new Promise((resolve, reject) => {
      axios.post(baseUrl + '/images/image-processing/', formData).then(function (response) {
        store.commit('setCanvasOutput', {"url": baseUrl + response.data});
        resolve(response);
      })
        .catch(error => {
          reject(error);
        })
    })
  },
  cancelFiltersChangesDialog(store,{removeImageUrl,dialog}){
     store.commit('closeDialog',dialog)
        axios.post(baseUrl + '/images/remove-image/', {"image_url": removeImageUrl}).catch(error => {
          console.log(error.response.data)
        })
  }
};
const getters = {
  getBackendImageUrl(state) {
    return state.backendImageUrl
  }
};
const mutations = {
  setImagesRef(state, refs) {
    state.refs = refs
  },
  setCanvasOutput(state, {url, filters = null}) {
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
  },
  openDialog(state, dialog) {
    console.log(dialog)
    state.dialogs[dialog] = true
  },
  closeDialog(state, dialog) {
    state.dialogs[dialog] = false
    if (dialog==="addNoise" || dialog==="removeNoise"){
      state.noiseRadioGroup=null
    }
  },
  setNoiseRadioGroup(state, value) {
    state.noiseRadioGroup = value
  },
  setRemoveRainRadius(state, value) {
    state.removeRainRadius = value
  },
  removeRainEpsilon(state, value) {
    state.removeRainEpsilon = value
  },
  setBackendImageUrl(state, url) {
    state.backendImageUrl = url
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
