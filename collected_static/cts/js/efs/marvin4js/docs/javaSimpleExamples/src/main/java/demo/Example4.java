package demo;

import gui.DemoPaneQuery;

import java.awt.BorderLayout;

import javax.swing.JFrame;

import service.TableService;
import service.TableServiceImpl;

public class Example4 {

	public static void main(String[] args) {
		Example4 cq=new Example4();
		cq.run();

	}

	private void run() {
		JFrame frame = new JFrame("Query Demo");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        TableService serv=new TableServiceImpl();

        frame.add(new DemoPaneQuery(serv), BorderLayout.CENTER);

        frame.pack();
        frame.setVisible(true);
		
	}

}
