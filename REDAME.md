# O projekcie
Aplikacja webowa pozwalająca na redukcje szumów pieprz i sól oraz gaussowskiego na obrazach cyfrowych oraz usunięciu smug deszczu. Szumy są usuwane przy użyciu sieci neuronowej, a smugi deszczu za pomocą algorytmu wykorzystującego wielokrotne zastosowanie filtra guided.

Aplikacja umożliwia wgranie przetwarzanego obrazu, sztuczne dodanie zakłóceń do obrazu postaci: szumu gaussowskiego (modelującego różne stopnie wypalenia piksela), szumu pieprz i sól (modelującego uszkodzone oraz prześwietlone fragmenty zdjęcia) oraz smug deszczu. System pozwala na usunięcie zakłóceń powstałych naturalnie lub sztucznie i zapisanie obrazu wynikowego. Ponadto do funkcjonalności należy zmiana kontrastu, jasności, nasycenia i barwy obrazu w celu korekty wizualnej zdjęcia spowodowanej operacją usuwania szumu.


### Pierwsze uruchomienie aplikacji
Należy uruchomić skrypty ./build_web_app_backend.sh oraz ./build_web_app_frontend.sh.
Następnie w folderze /frontend/app należy wykonać komendę npm install.
Potem należy uruchomić skrypt start_web_app.sh.

### Uruchomienie aplikacji
Należy uruchomić skrypt start_web_app.sh. Część frontendowa znajduje się pod adresem 127.0.0.1:8080, a backendowa na 127.0.0.1:8000.

### Zatrzymanie aplikacji
Należy uruchomić skrypt stop_web_app.sh.
