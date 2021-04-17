# O projekcie
Aplikacja webowa napisana w ramach pracy inżynierskiej. Aplikacja pozwala na redukcje szumów pieprz i sól oraz gaussowskiego, a także smug deszczu na obrazach cyfrowych. Szumy są usuwane przy użyciu wytrenowanej sieci neuronowej, a smugi deszczu za pomocą algorytmu wykorzystującego wielokrotne zastosowanie filtra guided.

Aplikacja umożliwia wgranie przetwarzanego obrazu, sztuczne dodanie zakłóceń do obrazu postaci: szumu gaussowskiego (modelującego różne stopnie wypalenia piksela), szumu pieprz i sól (modelującego uszkodzone oraz prześwietlone fragmenty zdjęcia) oraz smug deszczu. System pozwala na usunięcie zakłóceń powstałych naturalnie lub sztucznie i zapisanie obrazu wynikowego. Ponadto do funkcjonalności należy zmiana kontrastu, jasności, nasycenia i barwy obrazu w celu korekty wizualnej zdjęcia spowodowanej operacją usuwania szumu.

### Przykład usunięcia szumu pieprz i sól:
<img src="https://github.com/jsz5/denoising_app/blob/master/examples/sp03/noise.JPG" alt="noise_image" width=350/>
<img src="https://github.com/jsz5/denoising_app/blob/master/examples/sp03/denoised.JPG" alt="denoised_image" width=350/>

Przykłady pozostałych zakłóceń znajdują się w folderze ./examples

### Pierwsze uruchomienie aplikacji
Należy uruchomić skrypty ./build_web_app_backend.sh oraz ./build_web_app_frontend.sh.
Następnie w folderze /frontend/app należy wykonać komendę npm install.
Potem należy uruchomić skrypt start_web_app.sh.

### Uruchomienie aplikacji
Należy uruchomić skrypt start_web_app.sh. Część frontendowa znajduje się pod adresem 127.0.0.1:8080, a backendowa na 127.0.0.1:8000.

### Zatrzymanie aplikacji
Należy uruchomić skrypt stop_web_app.sh.

## Bibliografia
<a id="1">[1]</a> 
V. Lempitsky, A. Vedaldi and D. Ulyanov, "Deep Image Prior," 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition, Salt Lake City, UT, USA, 2018, pp. 9446-9454, doi: 10.1109/CVPR.2018.00984. https://dmitryulyanov.github.io/deep_image_prior

<a id="2">[2]</a>
Zheng, Xianhui & Liao, Yinghao & Guo, Wei & Fu, Xueyang & Ding, Xinghao. (2013). Single-Image-Based Rain and Snow Removal Using Multi-guided Filter. 258-265. 10.1007/978-3-642-42051-1_33. 
