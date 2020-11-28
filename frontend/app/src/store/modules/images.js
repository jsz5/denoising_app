const state = {
  refs: null,
  fileUploadDialog: false,
  addNoiseDialog: false,
  resultMat: null,
  noiseRadioGroup: null,
  showFilter: null,
  resultObjectUrl: null


};

const actions = {
  newImage(store, sourceImage) {
    store.commit('newImage', sourceImage);
    store.commit('cancelUploadFile');
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
  newImage(state, sourceImage) {
    let image_url = URL.createObjectURL(sourceImage)
    state.resultObjectUrl = URL.createObjectURL(sourceImage)
    state.refs.imageSrc.src = image_url
    var img = new Image();
    img.onload = function () {
      var ctx = state.refs.canvasOutput.getContext('2d');
      ctx.canvas.width = img.width
      ctx.canvas.height = img.height
      ctx.drawImage(img, 0, 0);
    }
    img.src = image_url
    console.log(img.src)
  },
  setOutputAsResult(state) {
    state.resultObjectUrl = state.refs.canvasOutput.toDataURL()
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
        state.resultObjectUrl = URL.createObjectURL(blob);
      });
    }
    img.src = state.resultObjectUrl

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
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
