const baseUrl = "http://127.0.0.1:8000"
const gaussian="gaussian"
const sp="sp"
const rain="rain"
const removeRain="remove_rain"
const contrast_and_brightness="contrast_and_brightness"

function clipValue(value) {
  if (value > 255) {
    value = 255
  }
  if (value < 0) {
    value = 0
  }
  return value
}

export {clipValue, baseUrl,gaussian,sp,rain,removeRain,contrast_and_brightness};