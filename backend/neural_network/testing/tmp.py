import os
import time

from neural_network.testing.denoising import Denoising

p = "./my_sp145"
o= "./result"


start = time.time()
for file in os.listdir(p):
    predicted = Denoising(f"{p}/{file}", noise="sp").denoise()
    predicted.save(f"{o}/{file}")
end = time.time()
t=end-start
print(t)
print(t/70)
