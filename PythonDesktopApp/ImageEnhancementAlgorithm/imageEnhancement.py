############################################################################################################################################

                                                                            #Receive the input
                                                                            
############################################################################################################################################

img = cv2.imread("SuperResolutionResult.png")
img_ref = cv2.imread("Kidney_000_Mıcroscope_4x_1.09_HuwDevıce.png")

############################################################################################################################################
                                                                           
                                                                            #Non Local Means Filtering 

############################################################################################################################################

sigma_est = np.mean(estimate_sigma(img, multichannel=True))  # get sigma values from all the channels

denoise_img = cv2.fastNlMeansDenoisingColored(img, None, sigma_est, sigma_est, 5, 21)


############################################################################################################################################

                                                                            #Histogram Matching 

############################################################################################################################################

matched = match_histograms(image=denoise_img, reference=img_ref, multichannel=True)

(B, G, R) = cv2.split(matched)

BB = match_histograms(image=B, reference=B, multichannel=False)
GB = match_histograms(image=G, reference=B, multichannel=False)
RB = match_histograms(image=R, reference=B, multichannel=False)

BG = match_histograms(image=B, reference=G, multichannel=False)  # Blue matched with green
GG = match_histograms(image=G, reference=G, multichannel=False)  # Green matched with green
RG = match_histograms(image=R, reference=G, multichannel=False)  # Red matched with green

BR = match_histograms(image=B, reference=R, multichannel=False)  # Blue matched with red
GR = match_histograms(image=G, reference=R, multichannel=False)  # Green matched with red
RR = match_histograms(image=R, reference=R, multichannel=False)  # Red matched with red


############################################################################################################################################

                                                                    #Histogram Matching Between Channels

############################################################################################################################################


out_refb = cv2.merge([BB, GB, RB])
out_refg = cv2.merge([BG, GG, RG])
out_refr = cv2.merge([BR, GR, RR])
print(BB.shape)


############################################################################################################################################

                                                                #PCA Map Extraction

############################################################################################################################################


PBB, PBG, PBR = pca_last.pca_weight_char(out_refb)
PGB, PGG, PGR = pca_last.pca_weight_char(out_refg)
PRB, PRG, PRR = pca_last.pca_weight_char(out_refr)

win_name = 'PCA Green'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0)
cv2.imshow(win_name, PGG)
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("PCA Green", PGG)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)




############################################################################################################################################

                                                                #Well Exposedness Map Extraction

############################################################################################################################################


EBB, EBG, EBR = well_exposedness(out_refb)
EGB, EGG, EGR = well_exposedness(out_refg)
ERB, ERG, ERR = well_exposedness(out_refr)

print(EGG.max())

win_name = 'Well Exposedness Green'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0)
cv2.imshow(win_name, EGG)
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("Well Exposedness Green", EGG)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)

############################################################################################################################################

                                                                #Brightness Map Extraction

############################################################################################################################################


DBB, DBG, DBR = well_exposedness(out_refb)
DGB, DGG, DGR = well_exposedness(out_refg)
DRB, DRG, DRR = well_exposedness(out_refr)


win_name = 'Brigtness Green'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0)
cv2.imshow(win_name, DGG)
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("Brightness Exposedness Green", DGG)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)

############################################################################################################################################

                                                                #Weight calculations

############################################################################################################################################

WBB = cv2.Laplacian((PBB * EBB * DBB), cv2.CV_64F)
WGB = cv2.Laplacian((PGB * EGB * DBB), cv2.CV_64F)
WRB = cv2.Laplacian((PRB * ERB * DRB), cv2.CV_64F)

WBG = cv2.Laplacian((PBG * EBG * DBG), cv2.CV_64F)
WGG = cv2.Laplacian((PGG * EGG * DGG), cv2.CV_64F)
WRG = cv2.Laplacian((PRG * ERG * DRG), cv2.CV_64F)

WBR = cv2.Laplacian((PBR * EBR * DBR), cv2.CV_64F)
WGR = cv2.Laplacian((PGR * EGR * DGR), cv2.CV_64F)
WRR = cv2.Laplacian((PRR * ERR * DRR), cv2.CV_64F)

############################################################################################################################################

                                                                #Reconstructing the Color Channels

############################################################################################################################################

recons_B = ((RB * WRB) + (GB * WGB) + (BB * WBB)) / (WRB + WGB + WBB)
recons_G = ((RG * WRG) + (GG * WGG) + (BG * WBG)) / (WRG + WGG + WBG)
recons_R = ((RR * WRR) + (GR * WGR) + (BR * WBR)) / (WRR + WGR + WBR)

final_image = cv2.merge([recons_B, recons_G, recons_R])

Y, Cb, Cr = cbcr_transform(final_image)
refY, refCb, refCr = cbcr_transform(img_ref)

matched_Cb = match_histograms(image=Cb, reference=refCb, multichannel=False)
matched_Cr = match_histograms(image=Cr, reference=refCr, multichannel=False)

Y = np.asarray(Y, dtype=np.uint8)
matched_Cb = np.asarray(matched_Cb, dtype=np.uint8)
matched_Cr = np.asarray(matched_Cr, dtype=np.uint8)

final_YCbCr = cv2.merge([Y, matched_Cb, matched_Cr])
final_BGR = cv2.cvtColor(final_YCbCr, cv2.COLOR_YCrCb2BGR)

############################################################################################################################################

                                                                #Display Each Result

############################################################################################################################################



win_name = 'Original Image'
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0)
cv2.imshow(win_name, img)
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("Original", img)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)



win_name = 'Final YBCR'
img = cv2.rotate(final_YCbCr, cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(final_YCbCr,(1920,1080))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, final_YCbCr)
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("Final YBCR", final_YCbCr)
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)

win_name = 'FINAL BGR'
img = cv2.rotate(final_BGR , cv2.ROTATE_90_CLOCKWISE)
img = cv2.resize(final_BGR ,(750,1000))
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(win_name, 0, 0 )
cv2.imshow(win_name, final_BGR )
cv2.resizeWindow(win_name, 1920,1080)
cv2.imshow("FINAL RGB", final_BGR )
cv2.waitKey(0); cv2.destroyAllWindows()
cv2.waitKey(1)
 
