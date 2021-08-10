import pydicom as dicom
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import random
import streamlit as st
import math
#import all packages

st.set_option('deprecation.showPyplotGlobalUse', False)

def lowhigh(image):
    image.seek(0)
    dcm = dicom.read_file(image)
    sorted_dcm = list(dcm.pixel_array.flatten())
    sorted_dcm.sort()
    return sorted_dcm[sorted_dcm.count(sorted_dcm[0])], sorted_dcm[-1]


def colorizedcm(image, bounds, colors):
    if bounds != []:
        bounds = list(bounds)
        bounds.sort()
        if min(bounds) <= lowhigh(image)[0] or max(bounds) >= lowhigh(image)[1]:
            st.error(f'Bounds must be in between the lowest and highest value of the image ({lowhigh(image)[0]} and {lowhigh(image)[1]}).')
            return None
        for num in bounds:
            if bounds.count(num) > 1:
                st.error(f'Bounds must contain all unique elements. {num} is repeated.')
                return None
    image.seek(0)
    dcm = dicom.dcmread(image)
    dcm_image = dcm.pixel_array

    sorted_dcm = list(dcm_image.flatten())
    sorted_dcm.sort()
    second_lowest = sorted_dcm[sorted_dcm.count(sorted_dcm[0])]



    if bounds == []:
        groups = math.ceil((10-math.floor(sorted_dcm.count(-2048)/len(sorted_dcm) * 10))/2)+1
        diff = (sorted_dcm[-1]-second_lowest)/(groups)
        bounds = [second_lowest]
        for i in range(groups):
            bounds.append(math.trunc(bounds[-1]+diff))
    else:
        bounds.insert(0, second_lowest)
        bounds.append(dcm_image.max())

    if colors == []:
        colors = np.random.randint(0,255,(len(bounds)+1,3))
    else:
        colors = np.array(colors)
    colors = colors/255

    shaded_image = np.zeros((512,512,3))
    factor = 0.3
    for i in range(len(bounds)-1):
        upper = bounds[i+1]
        lower = bounds[i]
        color = colors[i]*255
        color_midpoint = (lower+upper)/2
        mask_lower = ((dcm_image < color_midpoint) & (dcm_image >= lower))
        mask_upper = ((dcm_image >= color_midpoint) & (dcm_image < upper))
        general_mask = ((dcm_image >= lower) & (dcm_image < upper))
        shadefactor = ((2*factor)/(upper-lower))*abs(dcm_image-color_midpoint)
        for v in range(3):
            changed_color = color[v] * (1 - shadefactor)
            np.putmask(shaded_image[:,:,v], mask_lower, changed_color)
            changed_color = color[v] + (255 - color[v]) * shadefactor
            np.putmask(shaded_image[:,:,v], mask_upper, changed_color)
        average_hu = np.mean(dcm_image, where=general_mask)
        std_hu = np.std(dcm_image, where=general_mask)
        print(average_hu, std_hu)


    shaded_image[dcm_image == dcm_image.min()] = [255,255,255]
    dcm_noborder = dcm_image[dcm_image != dcm_image.min()]

    f, [ax1, ax2, ax3] = plt.subplots(1,3, figsize=(8,5), gridspec_kw={'left':0.029, 'right':0.979, 'wspace':0.293,'width_ratios':[10, 1, 10]})


    im = ax1.imshow(shaded_image.astype(np.uint8), interpolation = 'bilinear')
    ax1.set_title(image.name)
    ax1.axis('off')


    cmap = mpl.colors.ListedColormap(colors)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds, spacing='proportional', orientation='vertical')
    ax2.yaxis.set_label_position("left")
    ax2.yaxis.tick_left()


    n = np.histogram(dcm_noborder, bins=bounds)[0].tolist()
    n.append(0)
    space = list(range(len(bounds)))
    ax3.bar(space, n, align='edge', color = colors)
    ax3.set_xticks(range(0,len(bounds)))
    ax3.set_xticklabels(bounds)
    plt.setp(ax3.get_xticklabels(), rotation=90, horizontalalignment='center')


    ax3.set_yticks([0,len(dcm_noborder)/2, len(dcm_noborder)])
    ax3.set_yticklabels([0,50,100])
    ax3.set_ylabel('Occurence Ratio [%]')
    return f

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

st.title('DICOM Colorizer')
rawimage = st.sidebar.file_uploader('Load DICOM image', type=['dcm'])
if rawimage:
    boundscheck = st.sidebar.checkbox('Choose bounds manually?')
    if boundscheck:
        boundsminmax = st.sidebar.write(f"Min = {lowhigh(rawimage)[0]}, Max = {lowhigh(rawimage)[1]}")
        txtbounds = st.sidebar.text_input('Enter bounds (split by commas): ')
    else:
        boundsminmax = st.sidebar.empty()
        txtbounds = st.sidebar.empty()
    colorcheck = st.sidebar.checkbox('Choose colors manually?')
    if colorcheck:
        if boundscheck:
            colorcols = st.sidebar.columns(len(list(txtbounds.split(',')))+1)
        else:
            rawimage.seek(0)
            dcm = dicom.dcmread(rawimage)
            flatten = list(dcm.pixel_array.flatten())
            groups = math.ceil((10-math.floor(flatten.count(-2048)/len(flatten) * 10))/2)+1
            colorcols = st.sidebar.columns(groups)
        colordict = {}
        for i, x in enumerate(colorcols):
            x.color_picker(str(i), key = str(i))
    else:
        colorcols = st.sidebar.empty()

    colorize = st.sidebar.button('Colorize')

    if colorize:
        colors = []
        bounds = []
        if colorcheck:
            for i, x in enumerate(colorcols):
                colors.append(hex_to_rgb(st.session_state[str(i)]))
        if boundscheck:
            bounds = list(txtbounds.split(','))
            for n in range(len(bounds)):
                bounds[n] = int(bounds[n])
        rawimage.seek(0)
        st.pyplot(colorizedcm(rawimage, bounds, colors))
else:
    boundscheck = st.sidebar.empty()
    boundsminmax = st.sidebar.empty()
    colorcheck = st.sidebar.empty()
    colorize = st.sidebar.empty()
