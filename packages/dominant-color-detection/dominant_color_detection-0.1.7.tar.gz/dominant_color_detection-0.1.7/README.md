# Dominant color detection

Simple package which detects colors in a provided image.
Works best with already segmented images.

## Usage

```
from dominant_color_detection import detect_colors
k = 3
img_path = '/path/to/your/image.jpg'

colors, ratios = detect_colors(img_path, k)
```
