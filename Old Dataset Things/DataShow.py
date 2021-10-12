import numpy as np # linear algebra
import matplotlib.pyplot as plt
import os

# give paths to data and open images, masks and types npy files
images = np.load(r'D:\Proje.Yazılım\not_github\file1_extracted\images.npy')
masks = np.load(r'D:\Proje.Yazılım\not_github\file1_extracted\masks.npy')
ty = np.load(r'D:\Proje.Yazılım\not_github\file1_extracted\types.npy')

# saving path that will make new files
path = "D:/Proje.Yazılım/not_github/1_categorised/"

# specify input types in npy files
images = images.astype(int)
masks = masks.astype(int)
ty = ty.astype(str)

# loop to extract data accordingly
for i in range(500, 1500):

    # separate each mask
    npp, inf, stc, dc, epi, bg = np.split(masks[i], 6, axis=2) #256x256 #uint8'e çevir!

    # separate each channel
    r, g, b = np.split(images[i], 3, axis=2)

    # turn masks to binary
    npp = (npp > 0)
    inf = (inf > 0)
    stc = (stc > 0)
    dc = (dc > 0)
    epi = (epi > 0)
    bg = (bg > 0)

    # masking
    b1 = np.concatenate((np.multiply(r,npp), np.multiply(g,npp), np.multiply(b,npp)), axis=2)
    b2 = np.concatenate((np.multiply(r,inf), np.multiply(g,inf), np.multiply(b,inf)), axis=2)
    b3 = np.concatenate((np.multiply(r,stc), np.multiply(g,stc), np.multiply(b,stc)), axis=2)
    b4 = np.concatenate((np.multiply(r,dc), np.multiply(g,dc), np.multiply(b,dc)), axis=2)
    b5 = np.concatenate((np.multiply(r,epi), np.multiply(g,epi), np.multiply(b,epi)), axis=2)
    b6 = np.concatenate((np.multiply(r,bg), np.multiply(g,bg), np.multiply(b,bg)), axis=2)

    # sum all the images to compare with the original
    try3 = np.add(b1,np.add(b2,np.add(b3,np.add(b4,np.add(b5,b6)))))



    # plotting
    fig = plt.figure()
    ax1 = fig.add_subplot(2,4,1)
    ax1.imshow(b1)
    plt.title("Neoplastic Cells")

    ax2 = fig.add_subplot(2,4,2)
    ax2.imshow(b2)
    plt.title("Inflammatory")

    ax3 = fig.add_subplot(2,4,3)
    ax3.imshow(b3)
    plt.title("Connective/Soft Tissue Cells")

    ax4 = fig.add_subplot(2,4,4)
    ax4.imshow(b4)
    plt.title("Dead Cells")

    ax5 = fig.add_subplot(2,4,5)
    ax5.imshow(b5)
    plt.title("Epithelial")

    ax6 = fig.add_subplot(2,4,6)
    ax6.imshow(b6)
    plt.title("Background")

    ax7 = fig.add_subplot(2,4,7)
    ax7.imshow(try3)
    plt.title("all masks summed")

    ax8 = fig.add_subplot(2,4,8)
    ax8.imshow(images[i])
    plt.title("original")

    plt.suptitle(ty[i], fontsize=24)

    figure = plt.gcf()  # get current figure
    figure.set_size_inches(32, 18)

    # creating files with the type if not exists
    os.chdir(path)
    if not os.path.exists(ty[i]):
        os.makedirs(ty[i])

    # save file to corresponding file
    os.chdir(path + ty[i])
    plt.savefig(ty[i] + "_" + str(i) + ".png", bbox_inches="tight")
    plt.close('all')
    print(ty[i] + "_" + str(i) + ".png")
