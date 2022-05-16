from skimage.exposure import match_histograms


def histogram_matching(denoised_img, reference_img):
    matched_img = match_histograms(image=denoised_img, reference=reference_img, multichannel=True)
    return matched_img
