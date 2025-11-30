import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Initializations
data_dir = os.path.join("data")
train_files = {
    "class1": ["p11.bmp", "p12.bmp", "p13.bmp"],
    "class2": ["p21.bmp", "p22.bmp", "p23.bmp"],
    "class3": ["p31.bmp", "p32.bmp", "p33.bmp"]
}
test_file = "unknown.bmp"
im_size = (64, 64)
region_size = 20
peak_size = 10

def process():
    """Finds best class for unknown image"""
    # Load test image
    test_im = cv.imread(os.path.join(data_dir, test_file))
    test_im_gr = cv.cvtColor(test_im, cv.COLOR_BGR2GRAY)
    test_im_rgb = cv.cvtColor(test_im, cv.COLOR_BGR2RGB)

    # Train filters
    filters = train_mace()

    # Calculate correlations and sharpness
    correlations = {}
    results = {}
    for label, filter in filters.items():
        correlation = apply_filter(test_im_gr, filter)
        sharpness = calc_peak_sharpness(correlation)
        correlations[label] = correlation
        results[label] = sharpness

    display_correlations(correlations)

    # Find sharpest peak (best correlation)
    best_class = sorted(results, key=results.get, reverse=True)[0]
    best_path = os.path.join(data_dir, train_files[best_class][0])
    best_template = cv.imread(best_path)
    best_template = cv.cvtColor(best_template, cv.COLOR_BGR2RGB)

    display_best(test_im_rgb, best_template, best_class)

# Training
def train_mace():
    """Creates MACE filters for each class of images"""
    filters = {}
    for label, files in train_files.items():
        images = list()
        for img_file in files:
            path = os.path.join(data_dir, img_file)
            image = cv.imread(path)
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            images.append(image)
        
        filter = create_filter(images)
        filters[label] = filter

    return filters


def create_filter(train_imgs):
    """Creates MACE filter for images"""
    # Inits
    img_shape = train_imgs[0].shape
    N = img_shape[0] * img_shape[1]
    num_images = len(train_imgs)

    # Vector matrix
    X = np.zeros((N, num_images), dtype=complex)
    for i, img in enumerate(train_imgs):
        img = img.astype(float) / 255.0

        fft_img = np.fft.fft2(img).flatten()
        X[:,i] = fft_img
    Xp = X.conjugate().transpose()

    # Diagonal matrix
    D = np.zeros((N, N), dtype=complex)
    for i in range(N):
        D[i, i] = np.mean(np.abs(X[i, :]) ** 2)

    D_inv = np.linalg.inv(D)

    # Column vector
    u = np.ones((num_images,1))

    # Calculation
    temp = np.matmul(Xp, D_inv)
    temp = np.matmul(temp, X)
    temp = np.linalg.inv(temp)
    
    h = np.matmul(D_inv, X)
    h = np.matmul(h, temp)
    h = np.matmul(h, u)

    return h.flatten()

# Inference
def apply_filter(test, filter: np.ndarray):
    """Applies MACE filter to get correlation"""
    test = test.astype(float) / 255.0

    fft_test = np.fft.fft2(test).flatten()
    correlation = fft_test*filter.conjugate()
    correlation_out = np.abs(np.fft.ifft2(correlation.reshape(im_size)))
    correlation_out = np.fft.fftshift(correlation_out)

    return correlation_out

def calc_peak_sharpness(correlation):
    """Finds sharpness of correlation"""
    height, width = correlation.shape
    center_y, center_x = height // 2, width // 2

    # Region
    half_region = region_size//2
    
    r_y_start = max(0, center_y - half_region)
    r_y_end = min(height, center_y + half_region)
    r_x_start = max(0, center_x - half_region)
    r_x_end = min(width, center_x + half_region)

    region = correlation[r_y_start:r_y_end, r_x_start:r_x_end]

    # Peak
    half_peak = peak_size // 2
    
    p_y_start = half_region - half_peak
    p_y_end = half_region + half_peak
    p_x_start = half_region - half_peak
    p_x_end = half_region + half_peak

    peak = region[p_y_start:p_y_end, p_x_start:p_x_end]

    # Peakless region
    mask = np.ones_like(region, dtype=bool)
    mask[p_y_start:p_y_end, p_x_start:p_x_end] = False
    region_pl = region[mask]
    

    # Calculation
    peak_max = np.max(peak)
    region_pl_mean = np.mean(region_pl)
    region_pl_std = np.std(region_pl)

    sharpness = (peak_max-region_pl_mean) / region_pl_std

    return sharpness

# Displays
def display_correlations(corellation_dict: dict):
    """Displays correlations in both 2D and 3D"""
    fig = plt.figure("Correlations", figsize=(15, 10))
    idx = 1
    
    # 2D 
    for category, correlation in corellation_dict.items():
        ax = plt.subplot(2, 3, idx)
        im = ax.imshow(correlation, cmap="jet")
        ax.set_title(f"Correlation with {category}")
        plt.colorbar(im, ax=ax)
        idx += 1
    
    # 3D 
    idx = 1
    for category, correlation in corellation_dict.items():
        ax = plt.subplot(2, 3, idx + 3, projection='3d')
        
        x = np.arange(correlation.shape[1])
        y = np.arange(correlation.shape[0])
        X, Y = np.meshgrid(x, y)
        
        surf = ax.plot_surface(X, Y, correlation, cmap='jet', alpha=0.8)
        
        ax.set_title(f"{category}")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Correlation')
        
        # Point of view
        ax.view_init(elev=10, azim=45)        
        idx += 1
    
    plt.show()

def display_best(test_im, best_template, best_class):
    """Displays the best class for uknown image with one template image"""
    plt.figure()
    plt.subplot(1,2,1)
    plt.imshow(test_im)
    plt.title("Unknown image")

    plt.subplot(1,2,2)
    plt.imshow(best_template)
    plt.title(f"Nearest class: {best_class}")

    plt.show()

if __name__ == "__main__":
    process()