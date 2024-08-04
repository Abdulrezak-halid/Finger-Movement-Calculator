import cv2

from misc import Display


class Button:
    """
    Düğmelerin eylemlerini açiklayan sinif.   
    """
    def __init__(self, position: tuple, width: int, height: int, value: int):
        self.position = position
        self.width = width
        self.height = height
        self.value = value

    def draw_button(self, img: None, rectangle_color: tuple, text_color: tuple, font_scale: float, thickness: int,
                    text_x_margin: int = 0, text_y_margin: int = 0):
        """
      Düğmeleri çizer.
    :param img: video karesini görüntüle
    :param dikdörtgen_renk: düğme dikdörtgen rengi
    :param text_color: düğme metni rengi
    :param font_scale: düğme yazi tipi ölçeği
    :param kalinliği: düğme metni kalinliği
    :param text_x_margin: x ekseni kenar boşluğu
    :param text_y_margin: y ekseni kenar boşluğu
    :dönüş: geçersiz
        """
        # Hizalama
        text_size = cv2.getTextSize(text=self.value, fontFace=cv2.FONT_HERSHEY_PLAIN,
                                    fontScale=font_scale, thickness=thickness)
        text_x = int(self.position[0] + self.width / 2 - text_size[1] + text_x_margin)
        text_y = int(self.position[1] + self.height / 2 + text_size[1] + text_y_margin)
        
        # Çizim
        cv2.rectangle(img=img, pt1=self.position, pt2=(self.position[0] + self.width, self.position[1] + self.height),
                      color=rectangle_color, thickness=cv2.FILLED)
        cv2.rectangle(img=img, pt1=self.position, pt2=(self.position[0] + self.width, self.position[1] + self.height),
                      color=Display.MAIN_BORDER_COLOR, thickness=Display.MAIN_THICKNESS)
        cv2.putText(img=img, text=self.value, org=(text_x, text_y), fontFace=Display.MAIN_FONT,
                    fontScale=font_scale, color=text_color, thickness=thickness)

    def check_click(self, x, y, img: None, rectangle_color: tuple, text_color: tuple, thickness: int,
                    text_x_margin: int = 0, text_y_margin: int = 0):
        """
     Tiklamayi izler.
    :param x: x ekseni parmaklarinin konumu
    :param y: y ekseni parmaklarinin konumu
    :param img: video karesini görüntüle
    :param dikdörtgen_renk: tiklamadan sonraki düğme dikdörtgen rengi
    :param text_color: tiklamadan sonraki düğme metni rengi
    :param kalinliği: tiklama sonrasi düğme metni kalinliği
    :param text_x_margin: x ekseni kenar boşluğu
    :param text_y_margin: y ekseni kenar boşluğu
    :return: Tiklanirsa doğru, aksi halde yanliş
        """
        if self.position[0] < x < self.position[0] + self.width and \
                self.position[1] < y < self.position[1] + self.height:
            self.draw_button(img=img, rectangle_color=rectangle_color, text_color=text_color,
                             font_scale=Display.MAIN_CLICKED_FONT_SCALE, thickness=thickness,
                             text_x_margin=text_x_margin, text_y_margin=text_y_margin)
            return True
        else:
            return False
