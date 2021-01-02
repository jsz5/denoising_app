const baseUrl = "http://127.0.0.1:8000"
const gaussian="gaussian"
const sp="sp"
const rain="rain"
const removeRain="remove_rain"
const contrast_and_brightness="contrast_and_brightness"
const color_balance="color_balance"

function clipValue(value) {
  if (value > 255) {
    value = 255
  }
  if (value < 0) {
    value = 0
  }
  return value
}

export {clipValue, baseUrl,gaussian,sp,rain,removeRain,color_balance,contrast_and_brightness};