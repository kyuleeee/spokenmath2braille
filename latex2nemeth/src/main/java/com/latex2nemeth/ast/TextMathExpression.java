package com.latex2nemeth.ast;


import com.latex2nemeth.symbols.NemethTable;

public class TextMathExpression extends Expression {

    // TODO: This has to be more complicated than a simple string, since a math text expression may contain another expression.
    protected String content;

    public TextMathExpression(String content, NemethTable table) {
        super(table);
        this.content = content;
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
        return " " + content + " ";
    }

  
}
