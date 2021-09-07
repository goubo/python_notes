# 图片最大值计算
def image_size(w, h, th, tw):
    if h <= th and w <= tw:
        return w, h, 1
    f = min(th / h, tw / w)
    return int(w * f), int(h * f), f


# 根据图片大小,文字大小,位置,自定义偏移量,计算实际偏移量
def text_offset(w, h, text_w, text_h, sticky):
    # 根据位置算出初始偏移量
    x, y = 0, 0
    if sticky == 'center':
        x = w / 2 - text_w / 2
        y = h / 2 - text_h / 2
    elif sticky == 'se':
        x = w - text_w
        y = h - text_h
    elif 'e' in sticky:
        x = w - text_w
    elif 's' in sticky:
        y = h - text_h
    if 'w' == sticky or 'e' == sticky:
        y = h / 2 - text_h / 2
    elif 's' == sticky or 'n' == sticky:
        x = w / 2 - text_w / 2

    return int(x), int(y)
