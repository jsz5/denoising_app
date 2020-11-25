const state = {
  refs: null,
  fileUploadDialog: false,
  addNoiseDialog: false,
  resultMat: null

};

const actions = {
  newImage(store, sourceImage) {
    store.commit('newImage', sourceImage);
    store.commit('cancelUploadFile');
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
    state.refs.imageSrc.src = URL.createObjectURL(sourceImage)
    console.log(state.refs)
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
  setResultMat(state,result){
    state.resultMat=result
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
