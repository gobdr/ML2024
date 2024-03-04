import enum
import easyocr as ocr  # easyocr для распознавания текста на изображении
import cv2  # opencv для обработки изображений


# Определение перечисления для поддерживаемых языков
class Language(enum.Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"


# Класс для сканирования изображений
class ImageScanner:
    # Инициализация с выбором языков и настройкой использования GPU
    def __init__(self, lang: list[Language], gpu: bool = True):
        # Создание экземпляра Reader из easyocr с выбранными языками
        self.reader = ocr.Reader([language.value for language in lang], gpu=gpu)

    # Метод для сканирования изображения и извлечения текста
    def scan_image(self, image_path: str, verbose: bool = False) -> list[str]:
        # Чтение изображения с помощью opencv
        image = cv2.imread(image_path)
        # Извлечение текста с изображения
        extracted_text = self.reader.readtext(image, paragraph=True)

        # Вывод информации и обработанных изображений, если включен режим verbose
        if verbose:
            for (bbox, text) in extracted_text:
                print(f"[INFO] : {text}")
                # Распаковка координат ограничивающего прямоугольника
                (tl, tr, br, bl) = bbox
                # Преобразование координат в целочисленные значения
                tl = (int(tl[0]), int(tl[1]))
                br = (int(br[0]), int(br[1]))
                # Отрисовка прямоугольника вокруг текста
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                # Отрисовка извлеченного текста на изображении
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            # Отображение обработанного изображения
            cv2.imshow("Image", image)
            cv2.waitKey(0)

        # Возвращение списка извлеченных текстовых строк
        return [text for _, text in extracted_text]
