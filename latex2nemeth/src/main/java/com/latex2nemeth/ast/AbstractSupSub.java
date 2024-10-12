package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;

public abstract class AbstractSupSub extends Expression {
    public AbstractSupSub(){}

    public AbstractSupSub(NemethTable table){
        super(table);
    }

    //TODO: refactor
    String getSupSub(int code){
        if (code == SUP){
            return table.getMathCode("\\superscript");
        }
        else if (code == SUB) {
            return table.getMathCode("\\sub");
        }
        return "";
    }

 
}
