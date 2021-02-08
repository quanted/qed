package gui;

import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.ws.rs.core.Form;

import util.ResultTableModel;
import service.TableService;


public class DemoPaneQuery extends JPanel implements ActionListener {
	private static final String QUERY_COMMAND = "query";
	TableService serv;
	JTextArea request;
	ResultTableModel tableModel;
	
	public DemoPaneQuery(TableService serv) {
		super(new GridLayout(3, 1));
		
		tableModel=new ResultTableModel();
		List<String> labels=new ArrayList<String>();
		labels.add("Id");
		labels.add("Drug Bank Id");
		labels.add("Similarity");
		labels.add("SMILES");
		labels.add("Brand");
		tableModel.setLabels(labels);
		this.serv=serv;
		request=new JTextArea();
		JButton doit=new JButton("Query");
		doit.addActionListener(this);
		doit.setActionCommand(QUERY_COMMAND);
		
		JTable table = new JTable();
		table.setModel(tableModel);
        table.setPreferredScrollableViewportSize(new Dimension(500, 70));
        table.setFillsViewportHeight(true);

        //Create the scroll pane and add the table to it.
        JScrollPane scrollPane = new JScrollPane(table);

		add(request);
		add(doit);
		add(scrollPane);
	}


	public void actionPerformed(ActionEvent e) {
		if (QUERY_COMMAND.equals(e.getActionCommand())) {
			List<List<String>> data=serv.getTableContent(request.getText());
			tableModel.clearRows();
			tableModel.addTable(data);	
	    
	    }
	}

}
