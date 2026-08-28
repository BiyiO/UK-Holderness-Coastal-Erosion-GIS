import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, Polygon as MplPolygon, FancyArrow
from scipy.ndimage import gaussian_filter
from shapely.geometry import Point, LineString

# ==============================================================================
# 1. PATHS SETUP
# ==============================================================================
base_dir = r"C:\Users\USER\Documents\GIS\UK_Holderness_Coastal_Erosion"
dem_path = os.path.join(base_dir, "01_Raw_Data", "Coastal_DEM", "Holderness_DEM_30m.tif")
output_dir = os.path.join(base_dir, "04_Final_Maps")
os.makedirs(output_dir, exist_ok=True)

# Load DEM
with rasterio.open(dem_path) as src:
    dem = src.read(1).astype(np.float32)
    dem_bounds = src.bounds
    transform = src.transform
    crs = src.crs

# Load multi-temporal shorelines
sh_1990_path = os.path.join(base_dir, "02_Processed_Shorelines", "Holderness_Shoreline_1990_BNG.geojson")
sh_2026_path = os.path.join(base_dir, "02_Processed_Shorelines", "Holderness_Shoreline_2026_BNG.geojson")
gdf_1990 = gpd.read_file(sh_1990_path) if os.path.exists(sh_1990_path) else None
gdf_2026 = gpd.read_file(sh_2026_path) if os.path.exists(sh_2026_path) else None

# Clean DEM NoData / Water
dem_masked = np.where(dem < -50, np.nan, dem)

# ==============================================================================
# 2. COMPUTE MULTI-DIRECTIONAL HILLSHADE
# ==============================================================================
def compute_hillshade(elevation, azimuth_deg=315, altitude_deg=45, z_factor=3.5):
    # Gradients
    dx = np.gradient(elevation, 30.0, axis=1)
    dy = np.gradient(elevation, 30.0, axis=0)
    
    slope = np.arctan(z_factor * np.sqrt(dx**2 + dy**2))
    aspect = np.arctan2(-dx, dy)
    
    azimuth_rad = np.deg2rad(azimuth_deg)
    altitude_rad = np.deg2rad(altitude_deg)
    
    shaded = np.sin(altitude_rad) * np.cos(slope) + np.cos(altitude_rad) * np.sin(slope) * np.cos(azimuth_rad - aspect)
    shaded = (shaded - shaded.min()) / (shaded.max() - shaded.min() + 1e-6)
    return shaded

# Multi-angle blend for smooth cartographic relief
dem_smooth = gaussian_filter(np.nan_to_num(dem_masked, nan=0.0), sigma=1.0)
hs1 = compute_hillshade(dem_smooth, azimuth_deg=315, altitude_deg=45, z_factor=4.0)
hs2 = compute_hillshade(dem_smooth, azimuth_deg=225, altitude_deg=35, z_factor=2.5)
hillshade = 0.65 * hs1 + 0.35 * hs2

# ==============================================================================
# 3. MAP 1: OS / BGS STYLE TOPOGRAPHY & INFRASTRUCTURE MAP (Reference Image 2)
# ==============================================================================
print("Generating Map 1: Publication Topography & Infrastructure Map...")

# Custom Colormap: Deep Blue/Purple (0m) -> White (15-20m) -> Green (35-45m) -> Yellow (55-65m) -> Red (75-80m+)
colors_os = [
    (0.00, "#080b38"), # 0m deep marine / lowland base
    (0.08, "#1a237e"), # 5m
    (0.18, "#3949ab"), # 12m
    (0.28, "#c5cae9"), # 20m pale blue/lavender
    (0.35, "#ffffff"), # 25m white mid-tier
    (0.48, "#2e7d32"), # 38m green upland slope
    (0.65, "#fdd835"), # 52m yellow
    (0.82, "#fb8c00"), # 65m orange
    (1.00, "#d50000")  # 80m+ red wolds
]
cmap_os = mcolors.LinearSegmentedColormap.from_list("Holderness_OS_Topo", colors_os, N=256)
norm_os = mcolors.Normalize(vmin=0, vmax=80)

fig, ax = plt.subplots(figsize=(11, 15), facecolor='white', dpi=300)
ax.set_facecolor('#ffffff')

# Plot Hillshade and Elevation
ext = [dem_bounds.left, dem_bounds.right, dem_bounds.bottom, dem_bounds.top]
elev_rgb = cmap_os(norm_os(np.clip(dem_masked, 0, 80)))
# Blend with hillshade
blend = elev_rgb[:, :, :3] * hillshade[:, :, np.newaxis]
blend = np.clip(blend * 1.15, 0, 1)

# Mask ocean to crisp white / very light marine background for clean OS look
# Sea is generally where elevation is low and east of coast
ax.imshow(blend, extent=ext, origin='upper')

# Overlay Graticule / Ticks & Borders
ax.set_xlim(dem_bounds.left, dem_bounds.right)
ax.set_ylim(dem_bounds.bottom, dem_bounds.top)
ax.set_xticks(np.arange(510000, 550000, 10000))
ax.set_yticks(np.arange(410000, 480000, 10000))
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.tick_params(direction='in', length=7, width=1.5, colors='black', top=True, right=True)

# Double neatline border
for spine in ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(2.0)

# Settlement Locations (BNG Coordinates)
settlements = [
    ("Flamborough\nHead", 525300, 470600, 10, 'top', 'left'),
    ("Bridlington", 518200, 467500, 10, 'center', 'left'),
    ("Barmston", 517200, 459200, 8, 'center', 'left'),
    ("Skipsea", 516800, 455200, 8, 'center', 'left'),
    ("Hornsea", 520800, 447800, 10, 'center', 'left'),
    ("Mappleton", 522800, 444000, 8, 'center', 'left'),
    ("Aldbrough", 524500, 438600, 8, 'center', 'left'),
    ("Withernsea", 534200, 427800, 9, 'center', 'left'),
    ("Easington", 539800, 419200, 8, 'center', 'left'),
    ("Kilnsea", 541500, 415800, 8, 'center', 'left'),
    ("Spurn\nHead", 539500, 412000, 9, 'center', 'right'),
    ("Hull", 510000, 429000, 12, 'top', 'center'),
    ("Beverley", 503500, 439500, 9, 'center', 'left'),
    ("Driffield", 502200, 457800, 9, 'center', 'left'),
    ("Immingham", 519800, 415200, 9, 'center', 'left'),
    ("Grimsby", 527500, 409500, 9, 'center', 'left'),
    ("Cleethorpes", 530800, 408500, 9, 'center', 'left')
]

for name, x, y, size, va, ha in settlements:
    if dem_bounds.left <= x <= dem_bounds.right and dem_bounds.bottom <= y <= dem_bounds.top:
        # Town dot with halo
        ax.plot(x, y, 'o', color='black', markersize=6.5, markeredgecolor='white', markeredgewidth=1.2, zorder=5)
        offset_x = 700 if ha == 'left' else (-700 if ha == 'right' else 0)
        offset_y = -700 if va == 'top' else (700 if va == 'bottom' else 0)
        t = ax.text(x + offset_x, y + offset_y, name, fontsize=size, fontweight='bold', color='black', 
                    va=va, ha=ha, zorder=6)
        t.set_bbox(dict(facecolor='white', alpha=0.65, edgecolor='none', boxstyle='round,pad=0.15'))

# Critical Infrastructure Locations (Red Squares & Text)
infra = [
    ("Bridlington Harbour", 518300, 466300),
    ("Whitehill Gas Storage Facility (planned)", 521800, 440200),
    ("Aldbrough Gas Storage Facility", 523500, 437200),
    ("Out Newton Wind Farm", 538200, 421200),
    ("Easington Gas Terminal", 539800, 420000),
    ("Vessel Traffic Services\nHumber & Lifeboat Station", 540200, 410800)
]

for label, ix, iy in infra:
    if dem_bounds.left <= ix <= dem_bounds.right and dem_bounds.bottom <= iy <= dem_bounds.top:
        ax.plot(ix, iy, 's', color='#d50000', markersize=7.5, markeredgecolor='black', markeredgewidth=0.8, zorder=7)
        t = ax.text(ix + 900, iy, label, fontsize=8, fontweight='bold', color='#d50000', va='center', ha='left', zorder=8)
        t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.15'))

# Hornsea Waverider Buoy (Green Diamond)
bx, by = 527500, 447800
ax.plot(bx, by, 'D', color='#2e7d32', markersize=8.5, markeredgecolor='black', markeredgewidth=1.0, zorder=7)
t = ax.text(bx + 1100, by, "Hornsea waverider buoy", fontsize=8.5, fontweight='bold', color='#2e7d32', va='center', ha='left', zorder=8)
t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.15'))

# Prominent Geographic Labels
ax.text(536000, 455000, "NORTH\nSEA", fontsize=15, fontweight='bold', color='#1e293b', ha='center', va='center', zorder=4)
ax.text(522000, 434000, "H O L D E R N E S S", fontsize=15, fontweight='bold', color='white', rotation=-52, ha='center', va='center', alpha=0.85, zorder=4)
ax.text(524000, 418000, "Humber", fontsize=13, fontstyle='italic', fontweight='bold', color='#1e293b', rotation=-28, ha='center', va='center', zorder=4)
ax.text(510500, 412000, "Lincolnshire Wolds", fontsize=11, fontweight='bold', color='black', rotation=-45, ha='center', va='center', zorder=4)

# River Hull Label
ax.text(509500, 440000, "River Hull", fontsize=8.5, fontstyle='italic', color='black', rotation=78, ha='center', va='center', zorder=4)

# Top Right Notice & UK Inset Box
ax.text(dem_bounds.right - 800, dem_bounds.top - 800, 
        "Contains Ordnance Survey data\n© Crown copyright and database right 2026", 
        fontsize=7, color='black', ha='right', va='top', zorder=10,
        bbox=dict(facecolor='white', alpha=0.85, edgecolor='black', boxstyle='square,pad=0.3'))

# Draw UK Inset Map
inset_ax = fig.add_axes([0.68, 0.73, 0.22, 0.20])
inset_ax.set_facecolor('white')
inset_ax.set_xticks([])
inset_ax.set_yticks([])
for spine in inset_ax.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(1.2)

# Simplified UK Coastline Outline
uk_outline_x = [0.1, 0.25, 0.35, 0.45, 0.5, 0.6, 0.68, 0.72, 0.65, 0.62, 0.75, 0.8, 0.75, 0.65, 0.55, 0.5, 0.4, 0.3, 0.2, 0.15, 0.1]
uk_outline_y = [0.2, 0.15, 0.1, 0.15, 0.25, 0.3, 0.45, 0.6, 0.75, 0.88, 0.92, 0.7, 0.5, 0.35, 0.25, 0.15, 0.12, 0.2, 0.35, 0.4, 0.2]
inset_ax.plot(uk_outline_x, uk_outline_y, color='black', lw=1.2)
# Red locator square over East Yorkshire
inset_ax.add_patch(Rectangle((0.66, 0.52), 0.08, 0.08, facecolor='red', edgecolor='black', lw=1.0, zorder=5))

# Elevation Colorbar (Right Side)
cax = fig.add_axes([0.83, 0.22, 0.028, 0.45])
sm = plt.cm.ScalarMappable(cmap=cmap_os, norm=norm_os)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cax, ticks=np.arange(0, 85, 5))
cbar.set_label("Elevation\n(m OD)", fontsize=9.5, fontweight='bold', labelpad=10)
cbar.ax.tick_params(labelsize=8)

# Scalebar Bottom Right
scale_len_km = 15
scale_len_m = scale_len_km * 1000
sb_x = dem_bounds.right - 18000
sb_y = dem_bounds.bottom + 2500
sb_h = 1000

# Segmented scale bar
ax.add_patch(Rectangle((sb_x, sb_y), scale_len_m / 3, sb_h, facecolor='black', edgecolor='black', zorder=10))
ax.add_patch(Rectangle((sb_x + scale_len_m / 3, sb_y), scale_len_m / 3, sb_h, facecolor='white', edgecolor='black', zorder=10))
ax.add_patch(Rectangle((sb_x + 2 * scale_len_m / 3, sb_y), scale_len_m / 3, sb_h, facecolor='black', edgecolor='black', zorder=10))

ax.text(sb_x, sb_y + sb_h + 400, "0", fontsize=8, fontweight='bold', ha='center', zorder=11)
ax.text(sb_x + scale_len_m / 3, sb_y + sb_h + 400, "5", fontsize=8, fontweight='bold', ha='center', zorder=11)
ax.text(sb_x + 2 * scale_len_m / 3, sb_y + sb_h + 400, "10", fontsize=8, fontweight='bold', ha='center', zorder=11)
ax.text(sb_x + scale_len_m, sb_y + sb_h + 400, "15", fontsize=8, fontweight='bold', ha='center', zorder=11)
ax.text(sb_x + scale_len_m / 2, sb_y + sb_h + 1600, "Scale (km)", fontsize=10, fontweight='bold', ha='center', zorder=11)

map1_path = os.path.join(output_dir, "Holderness_Topography_Infrastructure_Map.png")
plt.savefig(map1_path, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"Saved Map 1 to: {map1_path}")

# ==============================================================================
# 4. MAP 2: 3D SHADED RELIEF & MULTI-TEMPORAL EROSION DYNAMICS (Reference Image 1)
# ==============================================================================
print("Generating Map 2: 3D Shaded Relief & Shoreline Retreat Dynamics...")

# Rainbow Bathy-Topo Colormap: Blue (-80 to 0) -> Cyan (0 to 40) -> Yellow/Green (80 to 120) -> Red/Orange (160 to 240)
colors_rainbow = [
    (0.00, "#0000ff"), # -80m Deep blue
    (0.25, "#00bfff"), # 0m Marine Cyan
    (0.50, "#00ff7f"), # 60m Green
    (0.70, "#ffff00"), # 120m Yellow
    (0.85, "#ff8c00"), # 180m Orange
    (1.00, "#ff0000")  # 240m Red
]
cmap_rainbow = mcolors.LinearSegmentedColormap.from_list("Holderness_Rainbow", colors_rainbow, N=256)
norm_rainbow = mcolors.Normalize(vmin=-40, vmax=140)

fig2, ax2 = plt.subplots(figsize=(11, 13), facecolor='white', dpi=300)
ax2.set_facecolor('#00bfff')

rgb_rainbow = cmap_rainbow(norm_rainbow(dem_masked))
blend_rainbow = rgb_rainbow[:, :, :3] * (hs1[:, :, np.newaxis]**1.2)
blend_rainbow = np.clip(blend_rainbow * 1.2, 0, 1)

ax2.imshow(blend_rainbow, extent=ext, origin='upper')

# Overlay Multi-Temporal Shorelines (1990 Cyan, 2026 Red)
if gdf_1990 is not None:
    gdf_1990.plot(ax=ax2, color='#ffffff', linewidth=2.2, linestyle='--', label='1990 Baseline Shoreline', zorder=6)
if gdf_2026 is not None:
    gdf_2026.plot(ax=ax2, color='#d50000', linewidth=2.5, label='2026 Active Shoreline (36-Yr Retreat)', zorder=7)

ax2.set_xlim(dem_bounds.left, dem_bounds.right)
ax2.set_ylim(dem_bounds.bottom, dem_bounds.top)
ax2.set_xticks(np.arange(510000, 550000, 10000))
ax2.set_yticks(np.arange(410000, 480000, 10000))
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax2.tick_params(direction='in', length=6, width=1.5, colors='black', top=True, right=True)

for spine in ax2.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(2.0)

# North Arrow
na_x = dem_bounds.right - 8000
na_y = dem_bounds.top - 6000
ax2.annotate('N', xy=(na_x, na_y), xytext=(na_x, na_y - 3500),
             arrowprops=dict(facecolor='black', edgecolor='black', width=3, headwidth=12),
             ha='center', va='bottom', fontsize=12, fontweight='bold', zorder=10)

# Colorbar
cax2 = fig2.add_axes([0.82, 0.45, 0.03, 0.35])
sm2 = plt.cm.ScalarMappable(cmap=cmap_rainbow, norm=norm_rainbow)
sm2.set_array([])
cbar2 = fig2.colorbar(sm2, cax=cax2, ticks=[-40, 0, 40, 80, 120, 140])
cbar2.set_label("Elevation\n(m OD)", fontsize=9.5, fontweight='bold', labelpad=10)
cbar2.ax.tick_params(labelsize=8)

# Scalebar Bottom Left
sb2_x = dem_bounds.left + 3000
sb2_y = dem_bounds.bottom + 25000
sb2_len = 10000 # 10 km
ax2.plot([sb2_x, sb2_x + sb2_len], [sb2_y, sb2_y], color='black', lw=3.0, zorder=10)
ax2.plot([sb2_x, sb2_x], [sb2_y - 500, sb2_y + 500], color='black', lw=2.0, zorder=10)
ax2.plot([sb2_x + 5000, sb2_x + 5000], [sb2_y - 500, sb2_y + 500], color='black', lw=2.0, zorder=10)
ax2.plot([sb2_x + sb2_len, sb2_x + sb2_len], [sb2_y - 500, sb2_y + 500], color='black', lw=2.0, zorder=10)
ax2.text(sb2_x, sb2_y + 800, "0", fontsize=8, fontweight='bold', ha='center', zorder=11)
ax2.text(sb2_x + 5000, sb2_y + 800, "5", fontsize=8, fontweight='bold', ha='center', zorder=11)
ax2.text(sb2_x + sb2_len, sb2_y + 800, "10", fontsize=8, fontweight='bold', ha='center', zorder=11)
ax2.text(sb2_x + 5000, sb2_y - 1500, "Kilometers", fontsize=9, fontweight='bold', ha='center', zorder=11)

ax2.legend(loc='lower right', facecolor='white', framealpha=0.9, edgecolor='black', fontsize=8.5)

map2_path = os.path.join(output_dir, "Holderness_3D_Hillshade_Erosion_Dynamics.png")
plt.savefig(map2_path, dpi=300, bbox_inches='tight')
plt.close(fig2)
print(f"Saved Map 2 to: {map2_path}")

print("All Custom Styled Maps Successfully Created!")
