const baseUrl = "http://127.0.0.1:8000"


function clipValue(value) {
  if (value > 255) {
    value = 255
  }
  if (value < 0) {
    value = 0
  }
  return value
}

export {clipValue, baseUrl};