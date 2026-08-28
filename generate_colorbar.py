import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

base_dir = r"C:\Users\USER\Documents\GIS\UK_Holderness_Coastal_Erosion"
output_dir = os.path.join(base_dir, "04_Final_Maps")
os.makedirs(output_dir, exist_ok=True)

# Custom Colormap: Deep Blue/Navy (0m) -> Lavender (12m) -> White (25m) -> Green (40m) -> Yellow (60m) -> Red (80m)
colors_os = [
    (0.00, "#080b38"), # 0m
    (0.08, "#1a237e"), # 5m
    (0.18, "#3949ab"), # 12m
    (0.28, "#c5cae9"), # 20m
    (0.35, "#ffffff"), # 25m
    (0.48, "#2e7d32"), # 40m
    (0.65, "#fdd835"), # 55m
    (0.82, "#fb8c00"), # 65m
    (1.00, "#d50000")  # 80m
]
cmap_os = mcolors.LinearSegmentedColormap.from_list("Holderness_Elevation_Ramp", colors_os, N=256)
norm_os = mcolors.Normalize(vmin=0, vmax=80)

# Create tall slim standalone colorbar with transparent background
fig, ax = plt.subplots(figsize=(1.8, 8.5), dpi=300)
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)

# Setup colorbar
sm = plt.cm.ScalarMappable(cmap=cmap_os, norm=norm_os)
sm.set_array([])

cbar = plt.colorbar(sm, cax=ax, orientation='vertical', ticks=np.arange(0, 85, 5))
cbar.set_label("Elevation\n(m OD)", fontsize=11, fontweight='bold', labelpad=12, family='sans-serif', color='black')
cbar.ax.tick_params(labelsize=9, length=5, width=1.2, colors='black', direction='out')
for label in cbar.ax.get_yticklabels():
    label.set_fontweight('bold')

# Black neatline around colorbar
cbar.outline.set_edgecolor('black')
cbar.outline.set_linewidth(1.5)

out_png = os.path.join(output_dir, "Holderness_Elevation_Colorbar_Legend.png")
plt.savefig(out_png, dpi=300, transparent=True, bbox_inches='tight')
plt.close(fig)
print(f"Generated standalone colorbar: {out_png}")
