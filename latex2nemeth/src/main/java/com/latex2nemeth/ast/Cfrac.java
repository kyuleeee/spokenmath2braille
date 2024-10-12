package com.latex2nemeth.ast;

import com.latex2nemeth.geom.Box;
import com.latex2nemeth.symbols.NemethTable;

/**
 * 
 * @author andpapas 
 * 
 * See Nemeth p. 80.
 */
public class Cfrac extends Fraction {

	public Cfrac(Expression num, Expression denom, NemethTable table) {
		super(num, denom, table);
		// TODO Auto-generated constructor stub
	}

	@Override
	public Box createBox() {
		
		Box box1 = this.numerator.createBox();
		Box box2 = this.denominator.createBox();
		
		int height1 = box1.getHeight();
		int height2 = box2.getHeight();

		int width1 = box1.getWidth();
		int width2 = box2.getWidth();
		
		
		Box b = new Box(Math.max(width1, width2), height1 + height2 + 1, height1);
		
		// Put the numerator on the top in the middle.
		b.insert(box1, (b.getWidth() - box1.getWidth())/2 , 0);
		
		// Create fraction line box...
		StringBuffer fline = new StringBuffer();
		
		for (int i = 0; i < b.getWidth(); i++) {
			fline.append("\u2812"); // Braille character 25
		}
		Box fbox= new Box(fline.toString());

		b.insert(fbox, 0, height1);
		
		
		b.insert(box2, (b.getWidth() - box2.getWidth())/2, height1+1);
		
		b.setBaselineHeight(height1);
		
		setBox(b);
				
		return b;

	}

}
