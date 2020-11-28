const state = {
  refs: null,
  fileUploadDialog: false,
  addNoiseDialog: false,
  resultMat: null,
  noiseRadioGroup: null,
  brightnessContrastDialog: false


};

const actions = {
  newImage(store, sourceImage) {
    store.commit('newImage', sourceImage);
    store.commit('cancelUploadFile');
  },


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
    state.refs.imageSrc.src = URL.createObjectURL(sourceImage)
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
    state.brightnessContrastDialog = true
  },
  cancelBrightnessContrastDialog(state) {
    state.brightnessContrastDialog = false
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
