let nhd_plus_layers = {
  "url": "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/export?",
  "layers": {
    "HUC2": {
      "dynamicLayers": [
        {
          "id": 5,
          "name": "Regions (HUC2)",
          "source": {
            "type": "mapLayer",
            "mapLayerId": 5
          },
          "drawingInfo": {
            "renderer": {
              "type": "simple",
              "label": "",
              "description": "",
              "symbol": {
                "color": [
                  255,
                  0,
                  0,
                  0
                ],
                "outline": {
                  "color": [
                    255,
                    0,
                    0,
                    255
                  ],
                  "width": 1.5,
                  "type": "esriSLS",
                  "style": "esriSLSSolid"
                },
                "type": "esriSFS",
                "style": "esriSFSSolid"
              }
            },
            "showLabels": false
          },
          "minScale": 0,
          "maxScale": 18489300
        }
      ],
      "dpi": 96,
      "transparent": true,
      "format": "png32",
      "layers": "show:5",
      "bbox": [
        -16223363.893430918,
        1268644.4680882622,
        -4678315.141240969,
        7256415.5158342365
      ],
      "bboxSR": 102100,
      "imageSR": 102100,
      "size": [
        1180,
        612
      ],
      "_ts": 1600871566665,
      "f": "image"
    },
    "HUC4": {
      "dynamicLayers": [
        {
          "id": 4,
          "name": "Subregions (HUC4)",
          "source": {
            "type": "mapLayer",
            "mapLayerId": 4
          },
          "drawingInfo": {
            "renderer": {
              "type": "simple",
              "label": "",
              "description": "",
              "symbol": {
                "color": [
                  255,
                  0,
                  0,
                  0
                ],
                "outline": {
                  "color": [
                    255,
                    0,
                    0,
                    255
                  ],
                  "width": 1.5,
                  "type": "esriSLS",
                  "style": "esriSLSSolid"
                },
                "type": "esriSFS",
                "style": "esriSFSSolid"
              }
            },
            "showLabels": false
          },
          "minScale": 18489299,
          "maxScale": 9244651
        }
      ],
      "dpi": 96,
      "transparent": true,
      "format": "png32",
      "layers": "show:4",
      "bbox": [
        -13542564.43741393,
        2423149.343307257,
        -7770040.061318956,
        5417034.867180245
      ],
      "bboxSR": 102100,
      "imageSR": 102100,
      "size": [
        1180,
        612
      ],
      "_ts": 1600873619223,
      "f": "image"
    },
    "HUC6": {
      "dynamicLayers": [
        {
          "id": 3,
          "name": "Basins (HUC6)",
          "source": {
            "type": "mapLayer",
            "mapLayerId": 3
          },
          "drawingInfo": {
            "renderer": {
              "type": "simple",
              "label": "",
              "description": "",
              "symbol": {
                "color": [
                  0,
                  0,
                  0,
                  0
                ],
                "outline": {
                  "color": [
                    255,
                    0,
                    0,
                    255
                  ],
                  "width": 1.5,
                  "type": "esriSLS",
                  "style": "esriSLSSolid"
                },
                "type": "esriSFS",
                "style": "esriSFSSolid"
              }
            },
            "showLabels": false
          },
          "minScale": 9244650,
          "maxScale": 4622326
        }
      ],
      "dpi": 96,
      "transparent": true,
      "format": "png32",
      "layers": "show:3",
      "bbox": [
        -12175258.875449061,
        3421111.184598254,
        -9288996.68740157,
        4918053.946534747
      ],
      "bboxSR": 102100,
      "imageSR": 102100,
      "size": [
        1180,
        612
      ],
      "_ts": 1600873850364,
      "f": "image"
    },
    "HUC8": {
      "dynamicLayers": [
        {
          "id": 2,
          "name": "Subbasins (HUC8)",
          "source": {
            "type": "mapLayer",
            "mapLayerId": 2
          },
          "drawingInfo": {
            "renderer": {
              "type": "simple",
              "label": "",
              "description": "",
              "symbol": {
                "color": [
                  0,
                  0,
                  0,
                  0
                ],
                "outline": {
                  "color": [
                    255,
                    0,
                    0,
                    255
                  ],
                  "width": 1.5,
                  "type": "esriSLS",
                  "style": "esriSLSSolid"
                },
                "type": "esriSFS",
                "style": "esriSFSSolid"
              }
            },
            "showLabels": false
          },
          "minScale": 4622325,
          "maxScale": 1155583
        }
      ],
      "dpi": 96,
      "transparent": true,
      "format": "png32",
      "layers": "show:2",
      "bbox": [
        -11722751.668000937,
        3867503.429783564,
        -10279620.573977195,
        4615974.810751811
      ],
      "bboxSR": 102100,
      "imageSR": 102100,
      "size": [
        1180,
        612
      ],
      "_ts": 1600874131853,
      "f": "image"
    },
    "HUC10": {
      "dynamicLayers": [
        {
          "id": 1,
          "name": "Watersheds (HUC10)",
          "source": {
            "type": "mapLayer",
            "mapLayerId": 1
          },
          "drawingInfo": {
            "renderer": {
              "type": "simple",
              "label": "",
              "description": "",
              "symbol": {
                "color": [
                  0,
                  0,
                  0,
                  0
                ],
                "outline": {
                  "color": [
                    255,
                    0,
                    0,
                    255
                  ],
                  "width": 1.5,
                  "type": "esriSLS",
                  "style": "esriSLSSolid"
                },
                "type": "esriSFS",
                "style": "esriSFSSolid"
              }
            },
            "showLabels": false
          },
          "minScale": 1155582,
          "maxScale": 577792
        }
      ],
      "dpi": 96,
      "transparent": true,
      "format": "png32",
      "layers": "show:1",
      "bbox": [
        -11151430.751250863,
        4087825.5126481606,
        -10790647.977745004,
        4274943.357890182
      ],
      "bboxSR": 102100,
      "imageSR": 102100,
      "size": [
        1180,
        612
      ],
      "_ts": 1600874258725,
      "f": "image"
    },
    "HUC12": {
      "dynamicLayers": [
        {
          "id": 0,
          "name": "Subwatersheds (HUC12)",
          "source": {
            "type": "mapLayer",
            "mapLayerId": 0
          },
          "drawingInfo": {
            "renderer": {
              "type": "simple",
              "label": "",
              "description": "",
              "symbol": {
                "color": [
                  0,
                  0,
                  0,
                  0
                ],
                "outline": {
                  "color": [
                    255,
                    0,
                    0,
                    255
                  ],
                  "width": 1.5,
                  "type": "esriSLS",
                  "style": "esriSLSSolid"
                },
                "type": "esriSFS",
                "style": "esriSFSSolid"
              }
            },
            "showLabels": false
          },
          "minScale": 577791,
          "maxScale": 0
        }
      ],
      "dpi": 96,
      "transparent": true,
      "format": "png32",
      "layers": "show:0",
      "bbox": [
        -11063375.294666458,
        4128184.2635826785,
        -10882983.907913376,
        4221743.18620377
      ],
      "bboxSR": 102100,
      "imageSR": 102100,
      "size": [
        1180,
        612
      ],
      "_ts": 1600874411308,
      "f": "image"
    }
  }
};