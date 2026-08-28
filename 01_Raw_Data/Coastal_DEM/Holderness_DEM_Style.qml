<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.28.0" styleCategories="AllStyleCategories">
  <pipe-data>
    <rasterrenderer type="singlebandpseudocolor" opacity="1" band="1" classificationMin="0" classificationMax="80">
      <rasterColorMap rampType="INTERPOLATED">
        <item value="0" color="#080b38" label="0 m (Lowlands/Coast)" alpha="255"/>
        <item value="5" color="#1a237e" label="5 m" alpha="255"/>
        <item value="12" color="#3949ab" label="12 m" alpha="255"/>
        <item value="20" color="#c5cae9" label="20 m" alpha="255"/>
        <item value="25" color="#ffffff" label="25 m" alpha="255"/>
        <item value="38" color="#2e7d32" label="38 m" alpha="255"/>
        <item value="52" color="#fdd835" label="52 m" alpha="255"/>
        <item value="65" color="#fb8c00" label="65 m" alpha="255"/>
        <item value="80" color="#d50000" label="80+ m (Yorkshire Wolds)" alpha="255"/>
      </rasterColorMap>
    </rasterrenderer>
    <brightnesscontrast brightness="10" contrast="15"/>
    <huesaturation colorizeGreen="128" colorizeRed="255" colorizeBlue="128" grayscaleMode="0" saturation="0" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
  </pipe-data>
  <blendMode>6</blendMode>
</qgis>
