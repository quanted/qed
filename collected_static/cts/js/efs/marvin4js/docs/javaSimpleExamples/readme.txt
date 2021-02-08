This set of examples demonstrates how ChemAxon Web Services can be used without including any ChemAxon specific jar.

The examples have simple swing user interface.
- The first example demonstrates a simple GET request to the Web Services root (status) page with Jersey Client library. 
It handles the get parameters as string.
- The second example lists the tables in a specific database and demonstrate how to decode json content with the help of 
GSON library.
- The third example shows how to post "multipart form data" request to import a molecule file.
- The last example demonstrates the usage of search option.

  We included a simple GSON serialization provider class in the util package. The example contains two GUI classes the 
DemoPaneSimple and DemoPaneQuery. The later one displays the search results in JTable. This GUI use the ResultTableModel 
util class to store the results.