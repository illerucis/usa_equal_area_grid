EARTHRADIUSKM = 6371.228
KILOMETERSOVERMILES = 1.60934

class USABoundsReference():

    MainlandWest = -125.421742
    MainlandEast = -65
    MainlandNorth = 49
    MainlandSouth = 24

    AlaskaWest = -169.050478
    AlaskaEast = -129
    AlaskaNorth = 71.5
    AlaskaSouth = 52.5

    HawaiiWest = -161.063126
    HawaiiEast = -153.905496
    HawaiiNorth = 22.25
    HawaiiSouth = 18.657159

    PuertoRicoWest = -67.541409
    PuertoRicoEast = -65.155191
    PuertoRicoNorth = 18.670957
    PuertoRicoSouth = 17.787452

    Geographies = {
        "Alaska": {
            "west": AlaskaWest,
            "east": AlaskaEast,
            "north": AlaskaNorth,
            "south": AlaskaSouth
        },
        "Hawaii": {
            "west": HawaiiWest,
            "east": HawaiiEast,
            "north": HawaiiNorth,
            "south": HawaiiSouth
        },
        "Mainland": {
            "west": MainlandWest,
            "east": MainlandEast,
            "north": MainlandNorth,
            "south": MainlandSouth
        },
        "PuertoRico": {
            "west": PuertoRicoWest,
            "east": PuertoRicoEast,
            "north": PuertoRicoNorth,
            "south": PuertoRicoSouth
        }
    }

def convert_arrays_of_geocos_to_kml(shape_arrays):

    kml_head = '''<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <Style id="clearPoly">
          <LineStyle>
            <width>0.0100</width>
          </LineStyle>
          <PolyStyle>
            <color>000000ff</color>
          </PolyStyle>
        </Style>'''

    kml_tail = '''</Document></kml>'''

    kml_individual_shape = '''
    <Placemark>
      <name>%s</name>
      <styleUrl>%s</styleUrl>
      <Polygon>
        <extrude>1</extrude>
          <altitudeMode>relativeToGround</altitudeMode>
            <outerBoundaryIs>
              <LinearRing>
                <coordinates>%s</coordinates>
              </LinearRing>
            </outerBoundaryIs>
      </Polygon>
    </Placemark>'''

    kml_individual_shapes = []

    for shape_array in shape_arrays:
        coordinates_for_kml = []

        for geoco in shape_array:
            coordinate = [str(geo) for geo in geoco]
            coordinate.append('0')
            coordinates_for_kml.append(','.join(coordinate))

        master_coordinate_string = '\n'.join(coordinates_for_kml)
        kml_individual_shapes.append(kml_individual_shape % ('1', '#clearPoly', master_coordinate_string))

    return ''.join([kml_head, ''.join(kml_individual_shapes), kml_tail])