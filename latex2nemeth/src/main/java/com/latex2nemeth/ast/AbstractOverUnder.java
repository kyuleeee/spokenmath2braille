package com.latex2nemeth.ast;

import com.latex2nemeth.symbols.NemethTable;

public abstract class AbstractOverUnder extends Expression {
    public AbstractOverUnder(){}

    public AbstractOverUnder(NemethTable table){
        super(table);
    }

    //TODO: refactor
    String getOverUnder(int code){
        if (code == OVER){
            return table.getMathCode("\\overset");
        }
        else if (code == UNDER) {
            return table.getMathCode("\\underset");
        }
        return "";
    }

 
}
