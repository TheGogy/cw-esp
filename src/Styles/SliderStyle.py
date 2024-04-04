def generateGradient(start, end):
    return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {start}, stop:1 {end})"

def generate_slider_style(color):
    '''Returns a string containing the QSlider CSS'''
    return f"""
        QSlider::groove:horizontal {{
            background: {color};
            border: 1px solid #D8DEE9;
            height: 7.5px;
            margin: 0px;
            border-radius: 4px;
        }}
        QSlider::handle:horizontal {{
            background: #D8DEE9;
            border: 1px solid #D8DEE9;
            width: 4px;
            height: 4px;
            margin: -4px 0;
            border-radius: 2px;
        }}
        QSlider::sub-page:horizontal {{
            background: {color};
        }}
        QSlider::add-page:horizontal {{
            background: #D8DEE9;
        }}
    """
    