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

import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.file.FileDataBodyPart;

import service.Service;


public class DemoPaneSimple extends JPanel implements ActionListener {
	Service serv;
	JTextArea request;
	JTextArea response;
	
	public DemoPaneSimple(Service serv) {
		super(new GridLayout(3, 1));
		
		this.serv=serv;

		request=new JTextArea();
		response=new JTextArea();
		
		JButton doit=new JButton("Call function");
		doit.addActionListener(this);
		doit.setActionCommand("call");
		
		add(request);
		add(doit);
		add(response);

	}

	public void actionPerformed(ActionEvent e) {
		if ("call".equals(e.getActionCommand())) {
			String data=serv.callFunc(request.getText());
			response.setText(data);
	    }
	}
}
