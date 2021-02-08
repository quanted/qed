package demo;

import gui.DemoPaneQuery;
import gui.DemoPaneSimple;

import java.awt.BorderLayout;

import javax.swing.JFrame;

import service.ServiceImportImpl;
import service.TableServiceImpl;
import service.Service;

public class Example3 {

	public static void main(String[] args) {
		Example3 cq=new Example3();
		cq.run();

	}

	private void run() {
		JFrame frame = new JFrame("Import");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        Service serv=new ServiceImportImpl();

        frame.add(new DemoPaneSimple(serv), BorderLayout.CENTER);

        frame.pack();
        frame.setVisible(true);
		
	}

}
