package com.latex2nemeth.ast;

import com.latex2nemeth.geom.Box;
import com.latex2nemeth.symbols.NemethTable;

import java.util.Vector;
import java.util.ArrayList;

public class MathExpression extends Expression {
	
	private Vector<Expression> children = new Vector<Expression>();
	
	
	public MathExpression(NemethTable table) {
		super(table);
	}

	public void addChild(Expression e) {
		children.add(e);
		e.setParent(this);
	}

	public Expression getChild(int i) {
		return children.elementAt(i);
	}
	
	public int getNumberOfChildren() {
		return children.size();
	}
	
	// Used for prime in setside
	public void replace(int pos, Expression exp) {
		children.set(pos,exp);
	}
	
	@Override
	public void assignFractionLevel() {
		int maxFraction = 0;
		for (Expression e : children) {
			e.assignFractionLevel();
			if (e.fractionlevel > maxFraction)
				maxFraction = e.fractionlevel;
		}
		// this level is the maximum of all other levels...
		this.fractionlevel = maxFraction;
	}

	@Override
	public void assignOtherLevels() {
		for (Expression e : children) {
			e.sqrtlevel = this.sqrtlevel;
			e.sublevel = this.sublevel;
			e.suplevel = this.suplevel;

			e.supsub = new ArrayList<>(this.supsub);

			e.assignOtherLevels();
		}
	}

	@Override
	public String getBraille() {
		StringBuffer buffer = new StringBuffer();
		for (Expression e : children) {
			buffer.append(e.getBraille());
		}
		return buffer.toString();
	}

	@Override
	public Box createBox() {
		int height = 0;
		int baseline = 0;
		int width = 0;
		for (Expression e : children) {
			e.createBox();

			int h = e.getBox().getHeight();
			int w = e.getBox().getWidth();
			int b = e.getBox().getBaselineHeight();

			if (h > height) // Get the maximum child width;
				height = h;
			if (b > baseline) // Get the maximum child width;
				baseline = b;
			width += w;
		}

		Box b = new Box(width, height, baseline);

		for (Expression e : children) {
			b.insertNext(e.getBox());
		}

		setBox(b);

		return this.box;

	}

	@Override
	Expression nextTo(Expression exp) {

		int index = children.indexOf(exp);
		if (index < children.size() - 1) {
			return children.get(index + 1);
		}

		return null;
	}

	public int getIntegerValue() throws NumberFormatException {
		int number = 0;
		int digit;
		for (int i = children.size() - 1; i >= 0; i--) {
			Expression exp = children.elementAt(i);
			if (exp instanceof SimpleExpression) {
				SimpleExpression sexp = (SimpleExpression) exp;

				String str = sexp.getTokenString();
				Character c = str.charAt(str.length() - 1);// Last sumbol...
				if (Character.isDigit(c)) {
					digit = Character.getNumericValue(c);
					number = digit + number * 10;
				} else
					throw new NumberFormatException();
			} else
				throw new NumberFormatException();
		}
		return number;
	}

	@Override
	public String getLabel() {
		String lbl = "";
		for (Expression child : children) {
			lbl = child.getLabel();
			if (!lbl.equals(""))
				break;
		}
		
		return lbl;
	}

}
