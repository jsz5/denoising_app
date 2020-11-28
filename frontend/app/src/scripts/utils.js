function clipValue(value) {
  if (value > 255) {
    value = 255
  }
  if (value < 0) {
    value = 0
  }
  return value
}
export {clipValue};