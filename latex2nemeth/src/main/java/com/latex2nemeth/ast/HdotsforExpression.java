package com.latex2nemeth.ast;

public class HdotsforExpression extends Expression {
	int hcols;

	public HdotsforExpression(int hcols) {
		this.hcols = hcols;
	}

	@Override
	public void assignFractionLevel() {
		// TODO Auto-generated method stub

	}

	@Override
	public void assignOtherLevels() {
		// TODO Auto-generated method stub

	}

	@Override
	public String getBraille() {
		// TODO Auto-generated method stub
		return "";
	}

	int getCols() {
		return this.hcols;
	}
}
