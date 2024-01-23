# -*- coding: utf-8 -*-
import seaborn as sns
import matplotlib.pyplot as plt
sns.set()
sns.set_theme(style="whitegrid")
#sns.set_palette("Accent")
plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"
EXT = ".pdf"
FIGSIZE = (8,5) # largura, altura
ENGLISH = False
SHOW_TITLE = False
SHOW_LEGEND = True

# Congresso
# EXT = ".svg"

#SWC
# FIGSIZE = (6,3) # largura, altura
ENGLISH = True
SHOW_TITLE = False
# SHOW_LEGEND = False


FIGSIZE_SM = (FIGSIZE[0]*0.8, FIGSIZE[1]*0.8) # largura, altura
FIGSIZE_HALF = (FIGSIZE[0]*0.5, FIGSIZE[1]*0.5) # largura, altura