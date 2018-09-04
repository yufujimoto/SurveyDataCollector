

// Make a cloud-free composite and display it.
var composite = ee.Algorithms.Landsat.simpleComposite({
  collection: l8raw.filterDate('2017-01-01', '2017-12-31'),
  asFloat: true
});

// Compute NDVI.
var ndvi = composite.normalizedDifference(['B5', 'B4']).rename('NDVI');
var ndbi = composite.normalizedDifference(['B6', 'B5']).rename('NDBI');

// Set up the maps.
var maps = [];

var map_ndvi = ui.Map();
var map_ndbi = ui.Map();

map_ndvi.addLayer(ndvi, {min: 0, max: 1, palette: ['white', 'green']}, 'ndvi');
map_ndbi.addLayer(ndbi, {min: -1, max: 0.5, palette: ['white', 'green']}, 'ndbi');

map_ndvi.setControlVisibility(false);
map_ndbi.setControlVisibility(false);

map_ndvi.add(ui.Label(label));
map_ndbi.add(ui.Label(label));

maps.push(map_ndvi);
maps.push(map_ndbi);

// Link the maps.
var linker = ui.Map.Linker(maps);

// Because they are linked, they all respond to this event.
maps[0].setCenter(139.5703, 35.7554, 8);

// Set everything in the root panel to the list of widgets.
ui.root.widgets().reset(maps);
