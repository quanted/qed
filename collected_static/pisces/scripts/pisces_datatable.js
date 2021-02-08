/**
 * Created by KWOLFE on 11/7/2016.
 */

var data_table = null;

fish_by_huc_columns = [
    {title: "Common Name"},
    {title: "Genus"},
    {title: "Species"},
    {title: "Max Size"},
    {title: "HUC"},
    {title: "Genus ID"},
    {title: "Cond L"},
    {title: "Cond U"},
    {title: "pH L"},
    {title: "PH U"},
    {title: "Width L"},
    {title: "Width U"},
    {title: "Slope L"},
    {title: "Slope U"},
    {title: "Area L"},
    {title: "Area U"},
    {title: "Depth L"},
    {title: "Depth U"},
    {title: "DO L"},
    {title: "DO U"},
    {title: "TSS L"},
    {title: "TSS U"},
    {title: "Genus"}
];

fish_properties_columns = [
    {title: "Species ID"},
    {title: "Genus ID"},
    {title: "Genus"},
    {title: "Species"},
    {title: "Common Name"},
    {title: "Group"},
    {title: "Native"},
    {title: "PFG Page"},
    {title: "Sportfishing"},
    {title: "NonGame"},
    {title: "Subsis Fish"},
    {title: "Pollut Tol"},
    {title: "Max Size"},
    {title: "Rarity"},
    {title: "Caves"},
    {title: "Springs"},
    {title: "Headwaters"},
    {title: "Creeks"},
    {title: "Sml Riv"},
    {title: "Med Riv"},
    {title: "Lrg Riv"},
    {title: "Lk Imp Pnd"},
    {title: "Swp Msh By"},
    {title: "Coast Ocea"},
    {title: "Riffles"},
    {title: "Run FloPool"},
    {title: "Pool Bckwtr"},
    {title: "Benthic"},
    {title: "Surface"},
    {title: "NrShre Litt"},
    {title: "OpnWtr Pelag"},
    {title: "Mud Slt Det"},
    {title: "Sand"},
    {title: "Gravel"},
    {title: "Rck Rub Bol"},
    {title: "Vegetation"},
    {title: "WdyD Brush"},
    {title: "ClearWater"},
    {title: "Turbid Water"},
    {title: "Warm Water"},
    {title: "Cool Water"},
    {title: "Cold Water"},
    {title: "Lowlands LGr"},
    {title: "Uplands HGr"},
    {title: "Locat Notes"},
    {title: "Habit Notes"}
];

function initDT(columns, dataset){
    //Construct the measurement table
    data_table = $('#fish_data_table').DataTable({
        data: dataset,
        columns: columns,
        "scrollX": true,
        // "bJQueryUI": true,
        "bDeferRender": true,
        "bInfo" : false,
        "bDestroy" : true,
        // "bFilter" : false,
        // "bPagination" : true
    });
    attachTableClickEventHandlers();
}

function attachTableClickEventHandlers(){
  // row/column indexing is zero based
  $("#fish_data_table thead tr th").click(function() {    
            col_num = parseInt( $(this).index() );
            console.log("column_num ="+ col_num );  
    });
    $("#fish_data_table tbody tr td").click(function() {    
            col_cell = parseInt( $(this).index() );
            row_cell = parseInt( $(this).parent().index() );   
            console.log("Row_num =" + row_cell + "  ,  column_num ="+ col_cell );
    });
};


//trying to add "download data" button. issue with jquery version?
// $(document).ready(function() {
//     $('#fish_data_table').DataTable( {
//         dom: 'Bfrtip',
//         buttons: [
//             'copy', 'csv', 'excel', 'pdf', 'print'
//         ]
//     } );
// } );