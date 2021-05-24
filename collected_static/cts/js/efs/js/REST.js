var REST = {
  // turns on ajax console messages
  debug: true,

  // set on init
  domain: "http://pnnl.cloudapp.net",
//  domain: "http://localhost:8111",

  Urls: {
    // jchem_kad urls
    insertUrl     : "/webservices/rest-v0/data/jchem_kad/table/kad/operation",
    detailUrl     : "/webservices/rest-v0/data/jchem_kad/table/kad/detail/",
    searchUrl     : "/webservices/rest-v0/data/jchem_kad/table/kad/search",
    imgUrl        : "/webservices/rest-v0/data/jchem_kad/table/kad/display/",

    // computed util urls
    exportUrl     : "/webservices/rest-v0/util/calculate/molExport",
    utilUrl       : "/webservices/rest-v0/util/detail",

    // EFS web services
    getMetabolitesUrl: "/efsws/rest/metabolizer",
    setMetabolitesUrl: "/efsws/rest/chemical/save-metabolites",
  },

  init: function() {
    REST.domain = Settings.getDomain();
  },

  Constants: {
    // advanced search const params
    DISSIM_THRESHOLD : 0.5,
    SEARCH_TYPE      : "SUBSTRUCTURE",
    ORDER_BY         : "-cd_id",
    RESULT_FIELDS    : ["cd_id","cd_formula","cd_molweight"],
    RESULT_LIMIT     : 2000,

    // img size
    IMGSIZE          : "_110x110.png",
  },

  Util: {
    
    DetailsBySmiles : function(mol) {
      // used with Marvin4JS
      // finds IUPAC, SMILES, MOLWEIGHT, FORMULA
      // use name, iupac, or smiles as input

      // post request
      var request = new Object();
      request.structures = [{ "structure" : mol }];
      request.display = {};
      request.display.include = ["structureData"];
      request.display.additionalFields = {
        "iupac": "chemicalTerms(name)",
        "formula": "chemicalTerms(formula)",
        "mass": "chemicalTerms(mass)",
        "smiles" : "chemicalTerms(molString('smiles'))"};
      request.display.parameters = {"structureData" : "mrv"};

      // ajax params
      var params = new Object();
      params.url = REST.domain + REST.Urls.utilUrl;
      //params.async = true;
      params.type = "POST";
      params.contentType = "application/json";
      params.data = request;

      return REST.ajax(params);
    },

    ImageBySmiles: function(mol) {
      // used with degrade.jsp
      // finds image: url & byte string
      // use name, iupac, or smiles as input

      // post request
      var request = new Object();
      request.structures = [{ "structure" : mol }];
      request.display = {};
      request.display.include = ["image"];
      request.display.parameters = {};
      request.display.parameters.image = {"width": 110, "height": 110};
      request.display.additionalFields = {"iupac": "chemicalTerms(name)"};

      // ajax params
      var params = new Object();
      params.url = REST.domain + REST.Urls.utilUrl;
      params.type = "POST";
      params.contentType = "application/json";
      params.data = request;

      return REST.ajax(params);
    },

    MrvToSmiles: function(mrv) {
      // accepts mrv from Marvin4JS
      // converts to smiles

      // post request
      var request = new Object();
      request.structure = mrv;
      request.inputFormat = "mrv";
      request.parameters = "smiles";

      // ajax params
      var params = new Object();
      params.url = REST.domain + REST.Urls.exportUrl;
      params.type = "POST";
      params.contentType = "application/json";
      params.data = request;

      return REST.ajax(params);
    }
  },

  DB: {
    SmilesToId: function(smiles) {
      // find mol id using smiles
      // this is technically an insert but duplicates aren't enabled
      // returns the cd_id ONLY

      // post request
      var mol = new Object();
      mol.operationType = "INSERT";
      mol.structure = smiles;

      // ajax params
      var params = new Object();
      params.url = REST.domain + REST.Urls.insertUrl;
      params.type = "POST";
      params.contentType = "application/json";
      params.data = mol;

      return JSON.stringify(ajaxCall(params).cd_id).replace("-","");
    },

    ImageById: function(cd_id) {
      // returns an img url
      return REST.domain + REST.Urls.imgUrl + cd_id + REST.Constants.IMGSIZE;
    },

    DetailsById: function(cd_id) {
      // given a cd_id
      // this will return the comprehensive details for a mol id

      var params = new Object();
      params.url = REST.domain + REST.Urls.detailUrl + cd_id;
      params.type = "GET";

      return REST.ajax(params);
    },

    AdvancedSearch: function(params) {
      // use restful services for search
      // should we pass in params or grab from html here? - pass them in

      // post request
      var request = new Object();
      request.searchOptions = {};
      request.searchOptions.queryStructure = params.smiles;
      request.searchOptions.dissimilarityThreshold = REST.Constants.DISSIM_THRESHOLD;
      request.searchOptions.searchType = params.searchType;
      //request.searchOptions.searchType = REST.Constants.SEARCH_TYPE;

      request.filter = {};
      request.filter.conditions = {};
      request.filter.conditions = params.conditions;
      request.filter.orderby = REST.Constants.ORDER_BY;

      request.paging = {};
      request.paging.offset = 0;
      request.paging.limit = REST.Constants.RESULT_LIMIT;

      request.display = {};
      request.display.include = REST.Constants.RESULT_FIELDS;

      // ajax params
      var params1 = new Object();
      params1.url = REST.domain + REST.Urls.searchUrl;
      params1.type = "POST";
      params1.contentType = "application/json";
      params1.data = request;

      return REST.ajax(params1);;
    },

    SimpleDetails: function(cd_id) {
      // post request
      var mol = new Object();
      mol.include = ["cd_id","format"];
      mol.parameters = {};
      mol.parameters.format = {};
      mol.parameters.format.inchiAux = true;
      mol.parameters.format.uniqueSmiles = false;

      // ajax params
      var params = new Object();
      params.url = REST.domain + REST.Urls.detailUrl + cd_id;
      params.type = "POST";
      params.contentType = "application/json";
      params.data = mol;

      return REST.ajax(params);
    }
  },

  Metabolizer: {
    getMetabolites: function(args) {
      // post request
      var request = {};
      request.structure = args.smiles;
      request.transformationLibraries = args.transLibs;
      request.generationLimit = args.genLimit;
      request.populationLimit = args.popLimit;
      request.likelyLimit = args.likelyLimit;
      request.excludeCondition = args.excludeCondition;
      request.generateImages = args.generateImages;

      // ajax params
      var params = new Object();
      params.url = REST.domain + REST.Urls.getMetabolitesUrl;
      params.type = "POST";
      params.contentType = "application/json";
      params.data = request;

      return REST.ajax(params);
    },

    saveMetabolites: function(args) {
      // post request
      var request = {};
      request.metabolites = args.metabolites;

      // ajax params
      var params = new Object();
      params.url = REST.domain + REST.Urls.setMetabolitesUrl;
      params.type = "POST";
      params.contentType = "application/json";
      params.data = request;

      return REST.ajax(params);
    }
  },

  jsonRepack: function(jsonobj) {
    return JSON.parse(JSON.stringify(jsonobj));
  },

  ajax: function(params) {
    var results;

    if (params.async == undefined) params.async = false;

    if ((params.url !== undefined) && (params.type !== undefined)) {
      jQuery.ajax({
        url : params.url,
        async : params.async,
        type : params.type,
        contentType : params.contentType,
        data : JSON.stringify(params.data),
        success : function(response) {
          results = REST.jsonRepack(response);
        },
        error : function(jqXHR, textStatus, errorThrown) {
          results = "Fail ";
          console.log(" " + JSON.stringify(errorThrown));
        }
      });
    } else {
      results = "One or more params was undefined. No Ajax for you.";
    }

    // turn on for debug
    if (REST.debug) {
      console.log(JSON.stringify(params));
      console.log(JSON.stringify(results));
    }

    return results;
  }
};
