import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import easyocr

def id_template(path):
    """
    Prepare id template
    """
    # Load image
    template_path = os.path.join(path, "obcansky_prukaz_cr_sablona_2012_2014.png")
    temp_bgr = cv.imread(template_path)
    temp_gr = cv.cvtColor(temp_bgr, cv.COLOR_BGR2GRAY)
    # Sift - keypoints and descriptors
    sift = cv.SIFT.create()
    kp, des = sift.detectAndCompute(temp_gr, None)
    return (kp, des, temp_gr)


def process_ids(path):
    """
    Processes all ids
    """
    # Prepare template
    temp_kp, temp_des, temp_gr = id_template(path)

    # Test
    test_dir = os.path.join(path, "ids")
    tests = os.listdir(test_dir)
    for test in tests:
        test_path = os.path.join(test_dir, test)
        process_id(test_path,temp_gr , (temp_kp, temp_des))

def process_id(path,temp_gr ,template):
    """
    Processes an id into required state
    """
    # Load data
    temp_kp, temp_des = template
    test_bgr = cv.imread(path)
    test_gr = cv.cvtColor(test_bgr, cv.COLOR_BGR2GRAY)

    # SIFT test
    sift = cv.SIFT.create()
    kp, des = sift.detectAndCompute(test_gr, None)

    # Compare using 
    bf = cv.BFMatcher()
    matches = bf.knnMatch(temp_des, des, k=2)

    # Uncertainty filter
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    if len(good_matches) < 10:
        print("Nedostatek shod pro výpočet posunu/zarovnání")
        return
    
    # Transformation prediction
    src_pts = np.float32([temp_kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    matches_mask = mask.ravel().tolist()

    display_matches(temp_gr, temp_kp, test_gr, kp, matches_mask, good_matches)

    h,w = temp_gr.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv.perspectiveTransform(pts,M)


    # Recangle drawing
    detected = cv.polylines(test_gr.copy(), [np.int32(dst)], True, 255, 3, cv.LINE_AA)

    display_detected(detected)

    # Cut and align
    aligned = cv.warpPerspective(test_gr, np.linalg.inv(M), (w, h))

    display_aligned(aligned)

    # Cut parts
    photo_gr = aligned[66:202, 5:114]
    name_gr = aligned[50:80, 70:150]
    surname_gr = aligned[35:60, 70:150]

    display_parts(photo_gr, name_gr, surname_gr)

    # More contrast for OCR
    # _, name_bw = cv.threshold(name_gr, 0, 255, cv.THRESH_BINARY_INV)
    # _, surname_bw = cv.threshold(surname_gr, 0, 255, cv.THRESH_BINARY_INV)

    # OCR
    reader = easyocr.Reader(["cs", "en"])
    name_results = reader.readtext(name_gr)
    surname_results = reader.readtext(surname_gr)

    # Extract text
    name = name_results[0][1] if name_results else "not found!"
    surname = surname_results[0][1] if surname_results else "not found!"

    display_read(aligned, name, surname)

    plt.show()



# Displays
def display_matches(temp_gr, temp_kp, test_gr, test_kp, matches_mask, good):
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matches_mask, # draw only inliers
                   flags = 2)
    img3 = cv.drawMatches(temp_gr,temp_kp,test_gr,test_kp,good,None,**draw_params)

    plt.figure("Matches")
    plt.title("Detected matches")
    plt.imshow(img3, 'gray')
    # plt.show()

def display_detected(detected):
    plt.figure("Detected")
    plt.title("Detected id")
    plt.imshow(detected, cmap="gray")
    plt.axis('off')
    # plt.show()

def display_aligned(aligned):
    plt.figure("Aligned")
    plt.title("Aligned id")
    plt.imshow(aligned, cmap='gray')
    plt.axis('off')
    # plt.show()

def display_parts(photo, name, surname):
    plt.figure("Parts")
    plt.subplot(1,3,1)
    plt.imshow(photo, cmap="gray")
    plt.title("Photo")

    plt.subplot(1,3,2)
    plt.imshow(name, cmap="gray")
    plt.title("Name")

    plt.subplot(1,3,3)
    plt.imshow(surname, cmap="gray")
    plt.title("Surname")

    # plt.show()

def display_read(aligned, name, surname):
    text1 = f"jmeno: '{name}'"
    text2 = f"prijmeni: '{surname}'"
    aligned = aligned.copy()
    cv.putText(aligned, text1, (20,20), cv.FONT_HERSHEY_SIMPLEX,0.5, (255,0,0), 1)
    cv.putText(aligned, text2, (20,40), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

    plt.figure("Read id")
    plt.imshow(aligned, cmap="gray")
    # plt.show()

if __name__ == "__main__":
    data_dir = os.path.join("data")
    process_ids(data_dir)
