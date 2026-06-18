// Global variables
let originalImage = null;
let grayImageData = null;
let isProcessing = false;

// Kernel presets matching the Python version
const kernelPresets = {
    blur: [0.0625, 0.125, 0.0625, 0.125, 0.25, 0.125, 0.0625, 0.125, 0.0625],
    'sobel-bottom': [-1, -2, -1, 0, 0, 0, 1, 2, 1],
    emboss: [-2, -1, 0, -1, 1, 1, 0, 1, 2],
    identity: [0, 0, 0, 0, 1, 0, 0, 0, 0],
    'sobel-left': [0, 0, 0, 2, 0, -2, 1, 0, -1],
    outline: [-1, -1, -1, -1, 8, -1, -1, -1, -1],
    'sobel-right': [-1, 0, 1, -2, 0, 2, -1, 0, 1],
    sharpen: [0, -1, 0, -1, 5, -1, 0, -1, 0],
    'sobel-top': [1, 2, 1, 0, 0, 0, -1, -2, -1]
};

// DOM Elements
const imageInput = document.getElementById('imageInput');
const runProcessBtn = document.getElementById('runProcessBtn');
const runSlowBtn = document.getElementById('runSlowBtn');
const calcText = document.getElementById('calcText');
const originalCanvas = document.getElementById('originalCanvas');
const resultCanvas = document.getElementById('resultCanvas');
const stepCanvas = document.getElementById('stepCanvas');

const originalCtx = originalCanvas.getContext('2d');
const resultCtx = resultCanvas.getContext('2d');
const stepCtx = stepCanvas.getContext('2d');

// Initialize canvas sizes
function initCanvases() {
    const canvases = [originalCanvas, resultCanvas, stepCanvas];
    canvases.forEach(canvas => {
        canvas.width = 400;
        canvas.height = 400;
    });
}

// Get kernel values from inputs
function getKernelValues() {
    return [
        parseFloat(document.getElementById('v1').value),
        parseFloat(document.getElementById('v2').value),
        parseFloat(document.getElementById('v3').value),
        parseFloat(document.getElementById('v4').value),
        parseFloat(document.getElementById('v5').value),
        parseFloat(document.getElementById('v6').value),
        parseFloat(document.getElementById('v7').value),
        parseFloat(document.getElementById('v8').value),
        parseFloat(document.getElementById('v9').value)
    ];
}

// Set kernel values from preset
function setKernelValues(kernel) {
    const values = kernelPresets[kernel];
    if (values) {
        for (let i = 0; i < 9; i++) {
            document.getElementById(`v${i + 1}`).value = values[i];
        }
    }
}

// Convert image to grayscale
function toGrayscale(imageData) {
    const data = imageData.data;
    const grayData = new Uint8ClampedArray(data.length);
    
    for (let i = 0; i < data.length; i += 4) {
        const avg = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
        grayData[i] = avg;
        grayData[i + 1] = avg;
        grayData[i + 2] = avg;
        grayData[i + 3] = 255;
    }
    
    return grayData;
}

// Apply convolution to a single pixel
function applyConvolution(imageData, width, height, row, col, kernel) {
    let sum = 0;
    
    for (let kr = -1; kr <= 1; kr++) {
        for (let kc = -1; kc <= 1; kc++) {
            const r = row + kr;
            const c = col + kc;
            
            // Handle borders (treat out-of-bounds as 0)
            if (r >= 0 && r < height && c >= 0 && c < width) {
                const pixelIndex = (r * width + c) * 4;
                const kernelIndex = (kr + 1) * 3 + (kc + 1);
                sum += imageData[pixelIndex] * kernel[kernelIndex];
            }
        }
    }
    
    return Math.max(0, Math.min(255, sum));
}

// Full convolution process
function performConvolution(slowMode = false) {
    if (!grayImageData || isProcessing) return;
    
    isProcessing = true;
    const kernel = getKernelValues();
    
    const width = originalCanvas.width;
    const height = originalCanvas.height;
    
    // Create result image data
    const resultImageData = new ImageData(width, height);
    const stepImageData = new ImageData(width, height);
    
    // Copy original to step canvas
    stepImageData.data.set(grayImageData);
    
    if (slowMode) {
        // Slow mode - animate pixel by pixel
        let currentRow = 0;
        let currentCol = 0;
        
        function processNextPixel() {
            if (currentRow >= height - 1 || currentCol >= width - 1) {
                isProcessing = false;
                return;
            }
            
            const newValue = applyConvolution(grayImageData, width, height, currentRow, currentCol, kernel);
            const pixelIndex = (currentRow * width + currentCol) * 4;
            
            resultImageData.data[pixelIndex] = newValue;
            resultImageData.data[pixelIndex + 1] = newValue;
            resultImageData.data[pixelIndex + 2] = newValue;
            resultImageData.data[pixelIndex + 3] = 255;
            
            stepImageData.data[pixelIndex] = newValue;
            stepImageData.data[pixelIndex + 1] = newValue;
            stepImageData.data[pixelIndex + 2] = newValue;
            stepImageData.data[pixelIndex + 3] = 255;
            
            // Update calculation display
            updateCalcDisplay(currentRow, currentCol, newValue, kernel, grayImageData, width, height);
            
            // Draw to canvases
            resultCtx.putImageData(resultImageData, 0, 0);
            stepCtx.putImageData(stepImageData, 0, 0);
            
            currentCol++;
            if (currentCol >= width - 1) {
                currentCol = 0;
                currentRow++;
            }
            
            setTimeout(processNextPixel, 10); // Reduced delay for better performance
        }
        
        processNextPixel();
    } else {
        // Fast mode - process all pixels at once
        for (let r = 0; r < height - 1; r++) {
            for (let c = 0; c < width - 1; c++) {
                const newValue = applyConvolution(grayImageData, width, height, r, c, kernel);
                const pixelIndex = (r * width + c) * 4;
                
                resultImageData.data[pixelIndex] = newValue;
                resultImageData.data[pixelIndex + 1] = newValue;
                resultImageData.data[pixelIndex + 2] = newValue;
                resultImageData.data[pixelIndex + 3] = 255;
            }
        }
        
        resultCtx.putImageData(resultImageData, 0, 0);
        stepCtx.putImageData(resultImageData, 0, 0);
        
        calcText.textContent = 'Convolution complete! Image processed with custom kernel.';
        isProcessing = false;
    }
}

// Update calculation display text
function updateCalcDisplay(row, col, newValue, kernel, imageData, width, height) {
    const getValue = (r, c) => {
        if (r < 0 || c < 0 || r >= height || c >= width) return 0;
        return imageData[(r * width + c) * 4];
    };
    
    const p1 = getValue(row - 1, col - 1);
    const p2 = getValue(row - 1, col);
    const p3 = getValue(row - 1, col + 1);
    const p4 = getValue(row, col - 1);
    const p5 = getValue(row, col);
    const p6 = getValue(row, col + 1);
    const p7 = getValue(row + 1, col - 1);
    const p8 = getValue(row + 1, col);
    const p9 = getValue(row + 1, col + 1);
    
    calcText.textContent = `Row: ${row}   Column: ${col}   New Pixel: ${newValue.toFixed(2)}
${p1} × ${kernel[0]} + ${p2} × ${kernel[1]} + ${p3} × ${kernel[2]} + 
${p4} × ${kernel[3]} + ${p5} × ${kernel[4]} + ${p6} × ${kernel[5]} + 
${p7} × ${kernel[6]} + ${p8} × ${kernel[7]} + ${p9} × ${kernel[8]}`;
}

// Load image from file input
function loadImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                // Set canvas size to match image (scaled)
                const scale = Math.min(400 / img.width, 400 / img.height);
                originalCanvas.width = img.width * scale;
                originalCanvas.height = img.height * scale;
                resultCanvas.width = img.width * scale;
                resultCanvas.height = img.height * scale;
                stepCanvas.width = img.width * scale;
                stepCanvas.height = img.height * scale;
                
                // Draw original image
                originalCtx.drawImage(img, 0, 0, originalCanvas.width, originalCanvas.height);
                
                // Convert to grayscale
                const imageDataObj = originalCtx.getImageData(0, 0, originalCanvas.width, originalCanvas.height);
                grayImageData = toGrayscale(imageDataObj);
                
                // Display grayscale on all canvases
                originalCtx.putImageData(new ImageData(grayImageData, originalCanvas.width, originalCanvas.height), 0, 0);
                resultCtx.putImageData(new ImageData(grayImageData, resultCanvas.width, resultCanvas.height), 0, 0);
                stepCtx.putImageData(new ImageData(grayImageData, stepCanvas.width, stepCanvas.height), 0, 0);
                
                calcText.textContent = 'Image loaded successfully. Select a kernel and run convolution.';
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}

// Event listeners
imageInput.addEventListener('change', loadImage);

runProcessBtn.addEventListener('click', () => {
    if (grayImageData) {
        performConvolution(false);
    }
});

runSlowBtn.addEventListener('click', () => {
    if (grayImageData) {
        performConvolution(true);
    }
});

// Preset kernel buttons
document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const kernelType = btn.getAttribute('data-kernel');
        setKernelValues(kernelType);
        calcText.textContent = `Kernel "${kernelType}" loaded. Click "Run Process" to apply.`;
    });
});

// Initialize on load
initCanvases();
calcText.textContent = 'Click "Select Image" to load an image for convolution processing.';
