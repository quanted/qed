package util;

import java.util.ArrayList;
import java.util.List;

import javax.swing.table.AbstractTableModel;

public class ResultTableModel extends AbstractTableModel {
	
	
	private List<String> columnNames= new ArrayList<String>();
	
	private List<List<String>> data=new ArrayList<List<String>>();

	public ResultTableModel(){
		
	}
	
	public void setLabels(List<String> labels) {
		columnNames=labels;
	}
	
	
	public void clearRows() {
		data.clear();
		fireTableDataChanged();
	}

	public void addRow(List<String> dataRow) {
		addRowImpl(dataRow);
		fireTableDataChanged();
	}
	/**
	 * Internal row update code, does not trigger table data changed event!
	 * @param dataRow
	 */
	private void addRowImpl(List<String> dataRow) {
		if (columnNames.size()!=dataRow.size()) {
			throw new IllegalArgumentException("new row size must much with the table size");
		}
		data.add(dataRow);
	}
	
	public void addTable(List<List<String>> data) {
		for(List<String> dataRow:data){
			addRowImpl(dataRow);			
		}
		fireTableDataChanged();
	}
	
    public int getColumnCount() {
        return columnNames.size();
    }

    public int getRowCount() {
        return data.size();
    }

    public String getColumnName(int col) {
        return columnNames.get(col);
    }

    public Object getValueAt(int row, int col) {
        return data.get(row).get(col);
    }

    public Class getColumnClass(int c) {
        return getValueAt(0, c).getClass();
    }

    /*
     * Don't need to implement this method unless your table's
     * editable.
     */
    public boolean isCellEditable(int row, int col) {
        //Note that the data/cell address is constant,
        //no matter where the cell appears onscreen.
        if (col < 2) {
            return false;
        } else {
            return true;
        }
    }

    /*
     * Don't need to implement this method unless your table's
     * data can change.
     */
    public void setValueAt(Object value, int row, int col) {
        data.get(row).set(col, value.toString());
        fireTableCellUpdated(row, col);
    }
  
}