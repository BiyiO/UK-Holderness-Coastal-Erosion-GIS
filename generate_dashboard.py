import os
import json
import pandas as pd
import geopandas as gpd

base_dir = r"C:\Users\USER\Documents\GIS\UK_Holderness_Coastal_Erosion"
transect_geojson_path = os.path.join(base_dir, "03_DSAS_Transect_Analytics", "Holderness_DSAS_Transects_Complete.geojson")
comm_csv_path = os.path.join(base_dir, "03_DSAS_Transect_Analytics", "Holderness_Community_Vulnerability_Summary.csv")
erosion_poly_path = os.path.join(base_dir, "02_Processed_Shorelines", "Holderness_Net_Erosion_Polygons_1990_2026.geojson")
sh_1990_path = os.path.join(base_dir, "02_Processed_Shorelines", "Holderness_Shoreline_1990.geojson")
sh_2005_path = os.path.join(base_dir, "02_Processed_Shorelines", "Holderness_Shoreline_2005.geojson")
sh_2015_path = os.path.join(base_dir, "02_Processed_Shorelines", "Holderness_Shoreline_2015.geojson")
sh_2026_path = os.path.join(base_dir, "02_Processed_Shorelines", "Holderness_Shoreline_2026.geojson")

with open(transect_geojson_path, 'r', encoding='utf-8') as f:
    transects_geojson = json.load(f)

with open(erosion_poly_path, 'r', encoding='utf-8') as f:
    erosion_polys_geojson = json.load(f)

with open(sh_1990_path, 'r', encoding='utf-8') as f:
    sh_1990_geojson = json.load(f)

with open(sh_2026_path, 'r', encoding='utf-8') as f:
    sh_2026_geojson = json.load(f)

df_comm = pd.read_csv(comm_csv_path)
comm_data_json = df_comm.to_dict(orient='records')

df_transects = pd.read_csv(os.path.join(base_dir, "03_DSAS_Transect_Analytics", "Holderness_DSAS_Transect_Erosion_Rates.csv"))
transects_table_json = df_transects.to_dict(orient='records')

print(f"Loaded {len(transects_table_json)} transects and {len(comm_data_json)} communities.")

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Holderness Coast Coastal Erosion & Shoreline Retreat (1990 – 2026) | Web GIS Dashboard</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #0b111e;
            color: #e2e8f0;
        }}
        h1, h2, h3, h4, .font-heading {{
            font-family: 'Outfit', sans-serif;
        }}
        .glass-card {{
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(51, 65, 85, 0.6);
        }}
        .glass-card-glow {{
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(56, 189, 248, 0.3);
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.08);
        }}
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #0f172a;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #334155;
            border-radius: 4px;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
            background: #475569;
        }}
        .leaflet-container {{
            background: #070d19;
        }}
        .leaflet-popup-content-wrapper {{
            background: rgba(15, 23, 42, 0.95);
            color: #ffffff;
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            backdrop-filter: blur(8px);
        }}
        .leaflet-popup-tip {{
            background: rgba(15, 23, 42, 0.95);
        }}
    </style>
</head>
<body class="h-screen flex flex-col overflow-hidden">

    <!-- Top Executive Navigation Bar -->
    <header class="h-16 bg-slate-900/90 border-b border-slate-800 px-6 flex items-center justify-between z-30 shrink-0">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-rose-600 via-amber-500 to-cyan-400 p-0.5 shadow-lg shadow-rose-500/20">
                <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                    <i data-lucide="waves" class="w-5 h-5 text-cyan-400"></i>
                </div>
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <h1 class="text-lg font-bold text-white tracking-tight">HOLDERNESS COAST MULTI-DECADAL COASTAL EROSION AUDIT</h1>
                    <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/30">1990 – 2026 Baseline</span>
                    <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">DSAS 120 Transects</span>
                </div>
                <p class="text-xs text-slate-400">Study Extent: Flamborough Head → Bridlington → Hornsea → Mappleton → Withernsea → Spurn Point (60.5 km)</p>
            </div>
        </div>

        <div class="flex items-center gap-3">
            <button onclick="toggleTerminalGroyneModal()" class="px-3.5 py-1.5 rounded-lg bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 border border-amber-500/40 text-xs font-semibold flex items-center gap-1.5 transition-all shadow-sm">
                <i data-lucide="alert-triangle" class="w-4 h-4"></i>
                Terminal Groyne Case Study
            </button>
            <button onclick="resetMapView()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-medium text-slate-300 flex items-center gap-1.5 transition-all">
                <i data-lucide="compass" class="w-4 h-4 text-cyan-400"></i>
                Reset Extent
            </button>
            <a href="Holderness_Coastal_Erosion_Report.md" target="_blank" class="px-3.5 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold flex items-center gap-1.5 transition-all shadow-md shadow-cyan-600/30">
                <i data-lucide="file-text" class="w-4 h-4"></i>
                Scientific Report
            </a>
        </div>
    </header>

    <!-- Main Workspace Layout -->
    <div class="flex-1 flex overflow-hidden">

        <!-- Left Interactive Sidebar (Analytics & Controls) -->
        <aside class="w-96 bg-slate-900/95 border-r border-slate-800 flex flex-col z-20 shrink-0 custom-scrollbar overflow-y-auto">
            
            <!-- Key Metric KPI Cards -->
            <div class="p-4 border-b border-slate-800 space-y-3">
                <div class="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                    <span>Multi-Decadal Audit (1990-2026)</span>
                    <span class="text-rose-400 flex items-center gap-1"><i data-lucide="activity" class="w-3.5 h-3.5"></i> 36 Years</span>
                </div>
                
                <div class="grid grid-cols-2 gap-2.5">
                    <div class="glass-card p-3 rounded-xl border border-slate-800/80">
                        <span class="text-[11px] text-slate-400 block font-medium">Total Land Lost</span>
                        <div class="text-lg font-bold text-rose-400 font-heading mt-0.5">551.4 ha</div>
                        <span class="text-[10px] text-slate-500">5.51 km² (15.3 ha/yr)</span>
                    </div>
                    <div class="glass-card p-3 rounded-xl border border-slate-800/80">
                        <span class="text-[11px] text-slate-400 block font-medium">Mean Retreat Rate</span>
                        <div class="text-lg font-bold text-amber-400 font-heading mt-0.5">1.70 m/yr</div>
                        <span class="text-[10px] text-slate-500">Regional Average</span>
                    </div>
                    <div class="glass-card p-3 rounded-xl border border-slate-800/80">
                        <span class="text-[11px] text-slate-400 block font-medium">Peak Starvation Rate</span>
                        <div class="text-lg font-bold text-rose-500 font-heading mt-0.5">3.95 m/yr</div>
                        <span class="text-[10px] text-slate-500">Cowden / Aldbrough</span>
                    </div>
                    <div class="glass-card p-3 rounded-xl border border-slate-800/80">
                        <span class="text-[11px] text-slate-400 block font-medium">Assets at 2100 Risk</span>
                        <div class="text-lg font-bold text-cyan-400 font-heading mt-0.5">531+ Units</div>
                        <span class="text-[10px] text-slate-500">+ Gas Terminal Margin</span>
                    </div>
                </div>
            </div>

            <!-- Quick-Fly Coastal Hotspot Navigator -->
            <div class="p-4 border-b border-slate-800">
                <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                    <i data-lucide="map-pin" class="w-3.5 h-3.5 text-cyan-400"></i>
                    <span>Coastal Hotspot Quick-Fly</span>
                </div>
                <div class="grid grid-cols-2 gap-1.5 text-xs">
                    <button onclick="flyToSpot(54.120, -0.080, 13, 'Flamborough Head')" class="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-750 text-left border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Flamborough</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">0.2 m/y</span>
                    </button>
                    <button onclick="flyToSpot(54.084, -0.190, 13, 'Bridlington')" class="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-750 text-left border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Bridlington</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">0.4 m/y</span>
                    </button>
                    <button onclick="flyToSpot(54.005, -0.220, 13, 'Barmston / Skipsea')" class="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-750 text-left border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Skipsea / Ulrome</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">2.2 m/y</span>
                    </button>
                    <button onclick="flyToSpot(53.910, -0.165, 13, 'Hornsea')" class="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-750 text-left border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Hornsea Town</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">0.4 m/y</span>
                    </button>
                    <button onclick="flyToSpot(53.865, -0.135, 14, 'Mappleton Groynes')" class="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-750 text-left border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Mappleton Def.</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">0.3 m/y</span>
                    </button>
                    <button onclick="flyToSpot(53.835, -0.105, 13, 'Cowden & Aldbrough')" class="p-2 rounded-lg bg-rose-950/40 hover:bg-rose-900/50 text-left border border-rose-500/40 text-rose-200 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Cowden Starv.</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-500/30 text-rose-300 font-bold">3.9 m/y</span>
                    </button>
                    <button onclick="flyToSpot(53.725, 0.035, 13, 'Withernsea')" class="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-750 text-left border border-slate-700/60 text-slate-300 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Withernsea</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">0.5 m/y</span>
                    </button>
                    <button onclick="flyToSpot(53.645, 0.115, 13, 'Easington Gas Terminal')" class="p-2 rounded-lg bg-amber-950/40 hover:bg-amber-900/50 text-left border border-amber-500/40 text-amber-200 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Easington Gas</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/30 text-amber-300">2.0 m/y</span>
                    </button>
                    <button onclick="flyToSpot(53.578, 0.144, 13, 'Spurn Point Spit')" class="col-span-2 p-2 rounded-lg bg-cyan-950/40 hover:bg-cyan-900/50 text-left border border-cyan-500/40 text-cyan-200 hover:text-white transition-all flex items-center justify-between">
                        <span class="font-medium">Spurn Point (Sand Spit Breach Zone)</span>
                        <span class="text-[10px] px-1.5 py-0.5 rounded bg-cyan-500/30 text-cyan-300 font-bold">Dynamic Spit</span>
                    </button>
                </div>
            </div>

            <!-- Layer Visibility Controls -->
            <div class="p-4 border-b border-slate-800">
                <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                    <i data-lucide="layers" class="w-3.5 h-3.5 text-cyan-400"></i>
                    <span>GIS Map Layers</span>
                </div>
                <div class="space-y-2 text-xs">
                    <label class="flex items-center justify-between p-2 rounded-lg bg-slate-800/40 border border-slate-800 cursor-pointer hover:bg-slate-800">
                        <span class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
                            <span>Net Land Loss (1990-2026 Area)</span>
                        </span>
                        <input type="checkbox" id="layerErosionPolys" checked onchange="toggleLayer('erosionPolys')" class="rounded border-slate-700 text-cyan-500 focus:ring-cyan-500">
                    </label>
                    <label class="flex items-center justify-between p-2 rounded-lg bg-slate-800/40 border border-slate-800 cursor-pointer hover:bg-slate-800">
                        <span class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded-full bg-cyan-400 inline-block"></span>
                            <span>DSAS Measurement Transects (120)</span>
                        </span>
                        <input type="checkbox" id="layerTransects" checked onchange="toggleLayer('transects')" class="rounded border-slate-700 text-cyan-500 focus:ring-cyan-500">
                    </label>
                    <label class="flex items-center justify-between p-2 rounded-lg bg-slate-800/40 border border-slate-800 cursor-pointer hover:bg-slate-800">
                        <span class="flex items-center gap-2">
                            <span class="w-3 h-0.5 bg-blue-400 inline-block"></span>
                            <span>1990 Baseline Shoreline</span>
                        </span>
                        <input type="checkbox" id="layerSh1990" checked onchange="toggleLayer('sh1990')" class="rounded border-slate-700 text-cyan-500 focus:ring-cyan-500">
                    </label>
                    <label class="flex items-center justify-between p-2 rounded-lg bg-slate-800/40 border border-slate-800 cursor-pointer hover:bg-slate-800">
                        <span class="flex items-center gap-2">
                            <span class="w-3 h-0.5 bg-red-500 inline-block"></span>
                            <span>2026 Active Shoreline</span>
                        </span>
                        <input type="checkbox" id="layerSh2026" checked onchange="toggleLayer('sh2026')" class="rounded border-slate-700 text-cyan-500 focus:ring-cyan-500">
                    </label>
                    <label class="flex items-center justify-between p-2 rounded-lg bg-slate-800/40 border border-slate-800 cursor-pointer hover:bg-slate-800">
                        <span class="flex items-center gap-2">
                            <span class="w-3 h-3 rounded-full bg-amber-400 inline-block"></span>
                            <span>Hazard Risk Buffer Zones (50/100yr)</span>
                        </span>
                        <input type="checkbox" id="layerBuffers" checked onchange="toggleLayer('buffers')" class="rounded border-slate-700 text-cyan-500 focus:ring-cyan-500">
                    </label>
                </div>
            </div>

            <!-- Future Climate & Sea Level Rise Simulator -->
            <div class="p-4 border-b border-slate-800">
                <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center justify-between">
                    <span class="flex items-center gap-1.5"><i data-lucide="sliders" class="w-3.5 h-3.5 text-cyan-400"></i> Climate Scenario Simulator</span>
                    <span id="simYearLabel" class="text-xs font-bold text-cyan-400">Year 2050</span>
                </div>
                
                <div class="space-y-3 text-xs">
                    <div>
                        <div class="flex justify-between text-[11px] text-slate-400 mb-1">
                            <span>Projection Target Year</span>
                            <span id="targetYearVal" class="font-bold text-white">2050 (+24 yrs)</span>
                        </div>
                        <input type="range" id="simYearSlider" min="2026" max="2100" value="2050" step="1" oninput="updateSimulation()" class="w-full accent-cyan-400 bg-slate-800 h-1.5 rounded-lg cursor-pointer">
                    </div>

                    <div>
                        <div class="flex justify-between text-[11px] text-slate-400 mb-1">
                            <span>Sea-Level Rise / Storminess Factor</span>
                            <span id="slrFactorVal" class="font-bold text-rose-400">1.15x (UKCP18 High)</span>
                        </div>
                        <input type="range" id="simSlrSlider" min="1.0" max="1.5" value="1.15" step="0.05" oninput="updateSimulation()" class="w-full accent-rose-500 bg-slate-800 h-1.5 rounded-lg cursor-pointer">
                    </div>

                    <!-- Simulated Outcomes Card -->
                    <div class="glass-card p-2.5 rounded-lg border border-slate-800 space-y-1.5">
                        <div class="flex justify-between items-center text-[11px]">
                            <span class="text-slate-400">Simulated Additional Land Loss:</span>
                            <span id="simLandLoss" class="font-bold text-rose-400">421.6 ha</span>
                        </div>
                        <div class="flex justify-between items-center text-[11px]">
                            <span class="text-slate-400">Mean Cliff Recession:</span>
                            <span id="simMeanRecession" class="font-bold text-amber-400">46.9 meters</span>
                        </div>
                        <div class="flex justify-between items-center text-[11px]">
                            <span class="text-slate-400">Peak Clifftop Recession:</span>
                            <span id="simPeakRecession" class="font-bold text-rose-500">109.0 meters</span>
                        </div>
                        <div class="flex justify-between items-center text-[11px]">
                            <span class="text-slate-400">Est. Economic Asset Threat:</span>
                            <span id="simEconThreat" class="font-bold text-cyan-300">£142.5 Million</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Transect Inspector Details (Dynamic on Click) -->
            <div class="p-4 flex-1">
                <div class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
                    <i data-lucide="search" class="w-3.5 h-3.5 text-cyan-400"></i>
                    <span>Selected Transect Inspector</span>
                </div>
                <div id="inspectorContent" class="glass-card p-3 rounded-xl border border-slate-800 text-xs space-y-2">
                    <p class="text-slate-400 italic text-[11px]">Click on any cross-shore transect on the map or chart to view detailed geomorphological and regression metrics.</p>
                </div>
            </div>

        </aside>

        <!-- Right Side Main Map & Dynamic Analytics Pane -->
        <main class="flex-1 flex flex-col overflow-hidden relative">

            <!-- Interactive Map Container -->
            <div id="map" class="flex-1 w-full h-full"></div>

            <!-- Bottom Floating Analytical Chart Drawer -->
            <div class="h-64 bg-slate-900/95 border-t border-slate-800 p-3 flex flex-col z-20 shrink-0">
                <div class="flex items-center justify-between mb-1.5 px-2">
                    <div class="flex items-center gap-2">
                        <i data-lucide="trending-down" class="w-4 h-4 text-rose-400"></i>
                        <h3 class="text-xs font-bold text-white uppercase tracking-wider">North-to-South DSAS Cliff Recession Rate Curve (Flamborough Head → Spurn Point)</h3>
                    </div>
                    <div class="flex items-center gap-4 text-[11px]">
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> End Point Rate (EPR m/yr)</span>
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-cyan-400"></span> Linear Regression (LRR m/yr)</span>
                        <span class="flex items-center gap-1.5"><span class="w-2.5 h-0.5 bg-amber-400"></span> Regional Mean (1.7 m/yr)</span>
                    </div>
                </div>
                <div class="flex-1 relative">
                    <canvas id="transectChart"></canvas>
                </div>
            </div>

        </main>

    </div>

    <!-- Terminal Groyne Syndrome Modal -->
    <div id="terminalGroyneModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
        <div class="glass-card-glow max-w-2xl w-full rounded-2xl p-6 border border-slate-700 text-slate-200 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-lg bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
                        <i data-lucide="alert-triangle" class="w-5 h-5"></i>
                    </div>
                    <h3 class="text-lg font-bold text-white font-heading">Terminal Groyne Syndrome & The Mappleton Dilemma</h3>
                </div>
                <button onclick="toggleTerminalGroyneModal()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>

            <div class="text-xs space-y-3 leading-relaxed text-slate-300">
                <p><strong class="text-white">What is Terminal Groyne Syndrome?</strong> In coastal engineering, constructing hard groynes traps sediment moving via longshore drift (southward along Holderness at ~200,000 m³/year). While this builds a protective beach updrift, it completely starves the coastline immediately downdrift of sediment, leaving unprotected cliffs exposed to direct, unbuffered wave attack.</p>
                
                <div class="p-3 rounded-xl bg-slate-950/60 border border-slate-800 grid grid-cols-2 gap-3 text-[11px]">
                    <div>
                        <span class="text-emerald-400 font-bold block mb-1">Mappleton Scheme (1991):</span>
                        <p class="text-slate-400">Cost: £2.0 Million. 2 granite rock groynes & 450m rock revetment. Result: Shoreline stabilized (<0.35 m/yr erosion), saving the B1242 highway.</p>
                    </div>
                    <div>
                        <span class="text-rose-400 font-bold block mb-1">Downdrift Impact (Cowden/Aldbrough):</span>
                        <p class="text-slate-400">Erosion accelerated to 3.5 – 4.0 m/yr (almost double the baseline). Massive cliff slumping at Grange Farm & RAF Cowden.</p>
                    </div>
                </div>

                <p><strong class="text-white">Management Lessons:</strong> Hard engineering in isolated rural sectors solves local cliff recession but transfers and magnifies the crisis down-drift, demonstrating the necessity of integrated Shoreline Management Plans (SMP2).</p>
            </div>

            <div class="flex justify-end pt-2">
                <button onclick="toggleTerminalGroyneModal()" class="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold">Understood</button>
            </div>
        </div>
    </div>

    <!-- Embedded Geospatial Data -->
    <script>
        const transectsGeoJSON = {json.dumps(transects_geojson)};
        const erosionPolysGeoJSON = {json.dumps(erosion_polys_geojson)};
        const sh1990GeoJSON = {json.dumps(sh_1990_geojson)};
        const sh2026GeoJSON = {json.dumps(sh_2026_geojson)};
        const transectsData = {json.dumps(transects_table_json)};
        const communitiesData = {json.dumps(comm_data_json)};
    </script>

    <!-- Dashboard Logic & Leaflet Setup -->
    <script>
        lucide.createIcons();

        // 1. Initialize Map
        const map = L.map('map', {{
            center: [53.86, -0.05],
            zoom: 10,
            zoomControl: false
        }});
        L.control.zoom({{ position: 'topright' }}).addTo(map);

        // Basemaps
        const darkBasemap = L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: '&copy; CartoDB &copy; OpenStreetMap',
            maxZoom: 19
        }}).addTo(map);

        const satelliteBasemap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
            attribution: '&copy; Esri &mdash; Earthstar Geographics',
            maxZoom: 19
        }});

        // Layer Groups
        const layerGroups = {{
            erosionPolys: L.geoJSON(erosionPolysGeoJSON, {{
                style: {{
                    color: '#ef4444',
                    weight: 1,
                    fillColor: '#dc2626',
                    fillOpacity: 0.55
                }}
            }}).addTo(map),

            sh1990: L.geoJSON(sh1990GeoJSON, {{
                style: {{
                    color: '#38bdf8',
                    weight: 2,
                    dashArray: '4, 4'
                }}
            }}).addTo(map),

            sh2026: L.geoJSON(sh2026GeoJSON, {{
                style: {{
                    color: '#f43f5e',
                    weight: 2.5
                }}
            }}).addTo(map),

            transects: L.geoJSON(transectsGeoJSON, {{
                style: function(feature) {{
                    return {{
                        color: feature.properties.Hazard_Color || '#f43f5e',
                        weight: 3.5,
                        opacity: 0.9
                    }};
                }},
                onEachFeature: function(feature, layer) {{
                    const p = feature.properties;
                    layer.bindTooltip(`<b>Transect #${{p.Transect_ID}}</b><br>${{p.Coastal_Zone}}<br>EPR: ${{p.EPR_Erosion_Rate_m_yr}} m/yr`, {{
                        sticky: true,
                        className: 'text-xs'
                    }});
                    layer.on('click', function() {{
                        inspectTransect(p);
                        highlightTransectOnChart(p.Transect_ID);
                    }});
                }}
            }}).addTo(map),

            buffers: L.layerGroup().addTo(map)
        }};

        // Add Key Landmark Markers
        communitiesData.forEach(c => {{
            const marker = L.circleMarker([getLat(c.Distance_km), getLon(c.Distance_km)], {{
                radius: 6,
                color: '#ffffff',
                weight: 1.5,
                fillColor: c.EPR_m_yr > 3.0 ? '#f43f5e' : (c.EPR_m_yr > 1.5 ? '#f59e0b' : '#10b981'),
                fillOpacity: 0.95
            }}).addTo(map);

            marker.bindPopup(`
                <div class="p-1 space-y-1 text-xs">
                    <h4 class="font-bold text-sm text-cyan-400">${{c.Community}}</h4>
                    <p class="text-slate-300"><b>Defense:</b> ${{c.Defense}}</p>
                    <p class="text-slate-300"><b>Erosion Rate:</b> <span class="text-rose-400 font-bold">${{c.EPR_m_yr}} m/yr</span></p>
                    <p class="text-slate-300"><b>36-Yr Retreat:</b> ${{c.36yr_Retreat_m}} meters</p>
                    <p class="text-slate-300"><b>Threatened Assets (2100):</b> <span class="text-amber-400 font-bold">${{c.Properties_At_Risk_2100}} units</span></p>
                    <p class="text-slate-400 text-[11px] mt-1 border-t border-slate-700 pt-1"><b>Key Threat:</b> ${{c.Infrastructure_Threat}}</p>
                </div>
            `);
        }});

        function getLat(dist) {{
            // Approximate latitude interpolator along Holderness arc
            return 54.120 - (dist / 60.5) * (54.120 - 53.578);
        }}
        function getLon(dist) {{
            // Approximate longitude interpolator
            return -0.080 - (dist / 60.5) * (-0.080 - 0.144);
        }}

        function toggleLayer(layerKey) {{
            const checkbox = document.getElementById('layer' + layerKey.charAt(0).toUpperCase() + layerKey.slice(1));
            if (checkbox.checked) {{
                map.addLayer(layerGroups[layerKey]);
            }} else {{
                map.removeLayer(layerGroups[layerKey]);
            }}
        }}

        function flyToSpot(lat, lon, zoom, name) {{
            map.flyTo([lat, lon], zoom, {{ duration: 1.2 }});
        }}

        function resetMapView() {{
            map.flyTo([53.86, -0.05], 10, {{ duration: 1.0 }});
        }}

        function toggleTerminalGroyneModal() {{
            const modal = document.getElementById('terminalGroyneModal');
            modal.classList.toggle('hidden');
        }}

        // 2. Transect Inspector
        function inspectTransect(p) {{
            const content = document.getElementById('inspectorContent');
            content.innerHTML = `
                <div class="space-y-2">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
                        <span class="font-bold text-white text-sm">Transect #${{p.Transect_ID}}</span>
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold" style="background-color: ${{p.Hazard_Color}}30; color: ${{p.Hazard_Color}};">${{p.Hazard_Class}}</span>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-[11px]">
                        <div>
                            <span class="text-slate-400 block">Distance from North:</span>
                            <span class="font-semibold text-slate-200">${{p.Distance_From_North_km}} km</span>
                        </div>
                        <div>
                            <span class="text-slate-400 block">Cliff Elevation:</span>
                            <span class="font-semibold text-cyan-300">${{p.Cliff_Elevation_m}} m AOD</span>
                        </div>
                        <div>
                            <span class="text-slate-400 block">End Point Rate (EPR):</span>
                            <span class="font-bold text-rose-400">${{p.EPR_Erosion_Rate_m_yr}} m/yr</span>
                        </div>
                        <div>
                            <span class="text-slate-400 block">Linear Reg. Rate (LRR):</span>
                            <span class="font-semibold text-cyan-400">${{p.LRR_Regression_Rate_m_yr}} m/yr</span>
                        </div>
                        <div>
                            <span class="text-slate-400 block">36-Yr Total Net Loss:</span>
                            <span class="font-bold text-white">${{p.NSM_Total_Retreat_m}} meters</span>
                        </div>
                        <div>
                            <span class="text-slate-400 block">Starvation Index:</span>
                            <span class="font-semibold text-amber-400">${{p.Downdrift_Starvation_Index}}</span>
                        </div>
                    </div>
                    <div class="border-t border-slate-800 pt-1.5 text-[11px] space-y-1">
                        <p><b>Zone:</b> <span class="text-slate-300">${{p.Coastal_Zone}}</span></p>
                        <p><b>Geology:</b> <span class="text-slate-400">${{p.Geology}}</span></p>
                        <p><b>Defense:</b> <span class="text-slate-400">${{p.Defense_Type}}</span></p>
                        <p><b>SMP2 Policy:</b> <span class="text-cyan-300 font-semibold">${{p.SMP_Policy}}</span></p>
                    </div>
                </div>
            `;
        }}

        // 3. Initialize North-to-South Profile Chart
        const ctx = document.getElementById('transectChart').getContext('2d');
        const labels = transectsData.map(t => t.Distance_From_North_km + ' km');
        const eprRates = transectsData.map(t => t.EPR_Erosion_Rate_m_yr);
        const lrrRates = transectsData.map(t => t.LRR_Regression_Rate_m_yr);

        const transectChart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: 'EPR Erosion Rate (m/yr)',
                        data: eprRates,
                        borderColor: '#f43f5e',
                        backgroundColor: 'rgba(244, 63, 94, 0.1)',
                        borderWidth: 2,
                        pointRadius: 2,
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: '#ffffff',
                        tension: 0.2
                    }},
                    {{
                        label: 'LRR Linear Regression (m/yr)',
                        data: lrrRates,
                        borderColor: '#38bdf8',
                        borderWidth: 1.5,
                        borderDash: [3, 3],
                        pointRadius: 0,
                        tension: 0.2
                    }},
                    {{
                        label: 'Mean Rate (1.70 m/yr)',
                        data: Array(labels.length).fill(1.70),
                        borderColor: '#facc15',
                        borderWidth: 1.2,
                        borderDash: [5, 5],
                        pointRadius: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    mode: 'index',
                    intersect: false
                }},
                plugins: {{
                    legend: {{ display: false }},
                    tooltip: {{
                        backgroundColor: 'rgba(15, 23, 42, 0.95)',
                        titleColor: '#38bdf8',
                        bodyColor: '#ffffff',
                        borderColor: 'rgba(56, 189, 248, 0.3)',
                        borderWidth: 1
                    }}
                }},
                scales: {{
                    x: {{
                        grid: {{ color: 'rgba(51, 65, 85, 0.25)' }},
                        ticks: {{ color: '#94a3b8', font: {{ size: 9 }}, maxTicksLimit: 15 }}
                    }},
                    y: {{
                        min: 0,
                        max: 4.5,
                        grid: {{ color: 'rgba(51, 65, 85, 0.25)' }},
                        ticks: {{ color: '#94a3b8', font: {{ size: 9 }} }}
                    }}
                }},
                onClick: (event, elements) => {{
                    if (elements.length > 0) {{
                        const idx = elements[0].index;
                        const t = transectsData[idx];
                        inspectTransect(t);
                        map.flyTo([getLat(t.Distance_From_North_km), getLon(t.Distance_From_North_km)], 13);
                    }}
                }}
            }}
        }});

        function highlightTransectOnChart(transectId) {{
            // Index in array is transectId - 1
            const idx = transectId - 1;
            transectChart.setActiveElements([{{ datasetIndex: 0, index: idx }}]);
            transectChart.render();
        }}

        // 4. Future Projection Simulator Function
        function updateSimulation() {{
            const targetYear = parseInt(document.getElementById('simYearSlider').value);
            const slrFactor = parseFloat(document.getElementById('simSlrSlider').value);
            const deltaYears = targetYear - 2026;

            document.getElementById('targetYearVal').innerText = `${{targetYear}} (+${{deltaYears}} yrs)`;
            document.getElementById('simYearLabel').innerText = `Year ${{targetYear}}`;
            document.getElementById('slrFactorVal').innerText = `${{slrFactor.toFixed(2)}}x (${{slrFactor > 1.2 ? 'Extreme SLR' : (slrFactor > 1.05 ? 'UKCP18 High' : 'Baseline')}})`;

            const meanEPR = 1.70;
            const peakEPR = 3.95;
            const annualRegionalHa = 15.32;

            const simLandLossHa = (annualRegionalHa * deltaYears * slrFactor).toFixed(1);
            const simMeanMeters = (meanEPR * deltaYears * slrFactor).toFixed(1);
            const simPeakMeters = (peakEPR * deltaYears * slrFactor).toFixed(1);
            const econThreatMillions = (parseFloat(simLandLossHa) * 0.34).toFixed(1);

            document.getElementById('simLandLoss').innerText = `${{simLandLossHa}} ha`;
            document.getElementById('simMeanRecession').innerText = `${{simMeanMeters}} meters`;
            document.getElementById('simPeakRecession').innerText = `${{simPeakMeters}} meters`;
            document.getElementById('simEconThreat').innerText = `£${{econThreatMillions}} Million`;
        }}

        // Auto-select first transect for inspector
        if (transectsData.length > 0) {{
            inspectTransect(transectsData[40]); // default to Cowden area
        }}
    </script>
</body>
</html>
"""

dash_path = os.path.join(base_dir, "Holderness_Coastal_Erosion_Dashboard.html")
with open(dash_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated Interactive Web GIS Dashboard: {dash_path}")
