package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;

public class SimpleExpression extends Expression {
    private String token;

    public SimpleExpression(String token, NemethTable table) {
        super(table);
        this.token = token;
    }

    @Override
    public void assignFractionLevel() {
    }

    @Override
    public void assignOtherLevels() {
    }

    @Override
    public String getBraille() {
        // TODO Auto-generated method stub
        String code = table.getMathCode(token);
        if (code == null) {
            System.out.println("MATH SYMBOL " + token + " not found.");
            return "";
        }
        return code;
    }

    public String getTokenString() {
        return this.token;
    }

    

}
