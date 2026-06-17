# 2D Convolution Visualizer

**Author**: Diego André Sant'Ana (diego.santana@ifms.edu.br)  
**Version**: 1.0.0  
**License**: MIT

A simple interactive 2D convolution visualizer for educational purposes. This application allows you to apply different convolution kernels to images and visualize the results in real-time, including a step-by-step mode to understand how convolution works pixel by pixel.

## 📋 Features

- **Interactive Kernel Selection**: Choose from predefined convolution kernels (Blur, Sobel, Emboss, Sharpen, Outline, Identity, etc.)
- **Custom Kernel Values**: Manually adjust each value in the 3x3 convolution matrix
- **Real-time Processing**: Apply convolution and see results instantly
- **Step-by-Step Mode**: Watch the convolution process pixel by pixel for educational purposes
- **Multiple Views**: Simultaneously view original image, processed result, and step-by-step processing

## 🔧 Requirements

### Python Version

- Python 2.7 or Python 3.x
- OpenCV (cv2)
- NumPy
- Pillow (PIL)
- scikit-image
- Tkinter (usually included with Python)

**Note**: Despite what older documentation might suggest, this application does **NOT** require TensorFlow, Keras, CUDA, or GPU libraries. It's a pure CPU-based implementation using OpenCV.

## 📦 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd convolution-2d
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. System dependencies

Make sure you have OpenCV installed on your system:

**Ubuntu/Debian:**
```bash
sudo apt-get install python-opencv
```

**macOS:**
```bash
brew install opencv
```

**Windows:**
Download and install from [OpenCV releases](https://opencv.org/releases/)

## 🚀 Usage

Run the Python script:

```bash
python pyConvolution2D.py
```

### How to Use the Application

1. **Select Image**: Click "Select Image" button and choose a JPG or PNG image
2. **Choose Kernel**: Select a predefined convolution kernel from the radio buttons:
   - Blur
   - Bottom Sobel
   - Emboss
   - Identity
   - Left Sobel
   - Outline
   - Right Sobel
   - Sharpen
   - Top Sobel
3. **Customize**: Optionally modify individual kernel values using the spinboxes
4. **Process**: 
   - Click "Run Process" for instant results
   - Click "Run Process Slowly" to see the step-by-step visualization

## 🎯 Available Kernels

| Kernel | Description |
|--------|-------------|
| Blur | Smooths the image by averaging neighboring pixels |
| Sobel (Various) | Edge detection in different directions |
| Emboss | Creates a 3D embossed effect |
| Identity | No change (original image preserved) |
| Outline | Detects edges and outlines |
| Sharpen | Enhances edges and details |

## 📁 Project Structure

```
convolution-2d/
├── pyConvolution2D.py      # Main Python application
├── jsConvolution2D/         # JavaScript/Electron version
│   ├── main.js             # Electron main process
│   ├── renderer.js         # Browser-side logic
│   ├── index.html          # UI interface
│   ├── styles.css          # Styling
│   └── package.json        # Node.js dependencies
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## 🌐 JavaScript Version

A JavaScript version built with Electron is also available! See the `jsConvolution2D/` directory for details.

### Running the JavaScript Version

```bash
cd jsConvolution2D
npm install
npm start
```

## 📝 Notes

- The application converts images to grayscale before processing
- Step-by-step mode includes a 0.7 second delay between pixels for visualization
- Border pixels are handled by treating out-of-bounds values as 0

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available under the MIT License.

---

**Educational Purpose**: This tool was created for the Computer Vision course to help understand how 2D convolution operations work in image processing.  
