package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;

public class MathLabelExpression extends TextMathExpression {

	public MathLabelExpression(String content, NemethTable table) {
		super(content, table);
		// TODO Auto-generated constructor stub
	}
	
	 @Override
	    public String getBraille() {
	        return content ;
	    }

}
