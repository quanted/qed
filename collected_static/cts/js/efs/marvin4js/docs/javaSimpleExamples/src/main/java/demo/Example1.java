package demo;

import gui.DemoPaneSimple;

import java.awt.BorderLayout;

import javax.swing.JFrame;

import service.ServiceTableListImpl;
import service.Service;
import service.ServiceMainImpl;

public class Example1 {

	public static void main(String[] args) {
		Example1 cq=new Example1();
		cq.run();

	}

	private void run() {
		JFrame frame = new JFrame("Example1");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        Service serv=new ServiceMainImpl();

        frame.add(new DemoPaneSimple(serv), BorderLayout.CENTER);

        frame.pack();
        frame.setVisible(true);
		
	}

}
