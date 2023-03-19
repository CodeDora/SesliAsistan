import sys # sys kütüphanesi, Python yorumlayıcısının ve işletim sisteminin farklı yapılandırmalarını ve etkin çalışma zamanı bilgilerini içerir.
import speech_recognition as sr #Bu kütüphane, Python programlarının sesli komutları işleyebilmesi için kullanılır. Sesli komutları algılamak için mikrofon kullanımını destekler.
import cv2 #OpenCV (Open Source Computer Vision) kütüphanesi için Python sürümüdür. Görüntü işleme, nesne algılama ve diğer birçok bilgisayar görüşü işlemi için kullanılır.
import pyttsx3 #Bu kütüphane, Python programları için metin konuşma motoru sağlar. Programların bilgisayar kullanıcılarıyla konuşmasını sağlar.
import os #Bu kütüphane, işletim sistemi fonksiyonlarına erişmek için kullanılır. Örneğin, dosya yollarını değiştirme, dosya oluşturma, dosya silme vb.
import webbrowser #Bu kütüphane, web tarayıcısı fonksiyonlarına erişmek için kullanılır. Örneğin, bir URL açma veya tarayıcıda arama yapma gibi işlemler için kullanılabilir.
import pywhatkit #Bu kütüphane, Python programları için bir dizi yardımcı işlev sağlar. Örneğin, arama yapmak, metin okumak, e-posta göndermek gibi işlemler için kullanılabilir.

from PyQt5.QtCore import Qt #Bu kütüphane, PyQt5 için temel sınıflar ve işlevler sağlar. PyQt5, Python için bir GUI (Graphical User Interface) kütüphanesidir.
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel #PyQt5 için kullanıcı arabirimi (UI) elemanlarını sağlar. Örneğin, pencere, etiket, düğme, çerçeve gibi elemanlar PyQt5.QtWidgets kütüphanesi altında bulunur.

# Ses tanıma motorunu oluşturma
r = sr.Recognizer()

# Sesli motoru oluşturma
engine = pyttsx3.init()

class Assistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.cap = None
             
    def initUI(self):
        """
        Arayüzü oluşturmak için ben PyQt5 kullanıyorum
        Kaynak değşiklik yapılmak istenirse tüm kod baştan sona tekrardan incelenmesi gerekir!
        """
        self.setWindowTitle("Sesli Asistan")
        self.setGeometry(100, 100, 300, 200)
        
        self.lbl = QLabel("Sesli asistana hoş geldiniz!", self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setGeometry(50, 20, 200, 30)
        
        self.btn = QPushButton("Başla", self)
        
        self.btn.setGeometry(50, 80, 200, 30)
        self.btn.clicked.connect(self.listen)
        
    def listen(self):
        """
        Kullanıcının söylediği komutları dinleyen fonksiyon bu kısımda yer alıyor.
        Olabildiğince düzenlemeye çalıştım.
        """
        self.lbl.setText("Komut bekleniyor...")
        with sr.Microphone() as source:
            audio = r.listen(source,phrase_time_limit=5)
            
        try:
            command = r.recognize_google(audio, language="tr-TR")
            self.lbl.setText(f"Komut alındı: {command}")
            self.execute(command.lower())
        except sr.UnknownValueError:
            self.lbl.setText("Sizi anlayamadım!")
        except sr.RequestError:
            self.lbl.setText("Bağlantı hatası!")
            
    def execute(self, command):
        """
        Kullanıcının verdiği komutları işleyen fonksiyon.
        """
        if "Merhaba Lara" in command:
            self.lbl.setText("Merhaba, nasıl yardımcı olabilirim?")
            
        elif "Görüşürüz" in command:
            self.lbl.setText("Görüşürüz İbrahim")
            QApplication.quit()

        elif "kamerayı aç" in command and "açma" not in command:
            self.lbl.setText("Kamera açılıyor...")
            self.cap = cv2.VideoCapture(0)
            while True:
                ret, frame = self.cap.read()
                if ret:
                    cv2.imshow("Kamera", frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            self.cap.release()
            cv2.destroyAllWindows()

        elif "kamerayı kapat" in command:
            self.lbl.setText("Kamera kapatılıyor...")
            if self.cap is not None:
                self.cap.release()
                cv2.destroyAllWindows()
            else:
                self.lbl.setText("Kamera zaten kapalı!")

        if "spotify aç" in command and "açma" not in command:
            os.system("start spotify")
            self.lbl.setText("Spotify açılıyor...")
        
        elif "spotify kapat" in command:
            os.system("taskkill /im spotify.exe /f")
            self.lbl.setText("Spotify kapatıldı.")

        elif "arama yap" in command.lower():
                engine.say("Aranacak terimi söyleyin.")
                engine.runAndWait()
                with sr.Microphone() as source:
                    search_term = r.listen(source)
                    term = r.recognize_google(search_term, language="tr-TR")
                pywhatkit.search(term)
                engine.say(f"{term} için sonuçlar bulundu!")        
        else:
            self.lbl.setText("Bunu yapamam.")
            
             
if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant = Assistant()
    assistant.show()
    sys.exit(app.exec_())
#unutmayayım diye not alıyorum
"""
if __name__ == "__main__":
----# PyQt5 uygulama objesi oluşturma
    app = QApplication(sys.argv)

----# Asistan arayüz nesnesi oluşturma
    assistant = Assistant()

----# Arayüzü görünür hale getirme
    assistant.show()

----# Uygulamayı çalıştırma
    sys.exit(app.exec_())
"""